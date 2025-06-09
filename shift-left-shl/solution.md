# SHL Challenge Solution

*The article details the solution provided by the winner of the [SHL challenge](https://fherma.io/challenges/661643316a54e9817d3706f6).*

**Author:** [Chi-Hieu Nguyen](https://www.linkedin.com/in/hieu-nguyen-ba6548316), University of Technology Sydney, Australia.

## Introduction

The objective of the challenge is to evaluate a bitwise shift left operation on an encrypted integer within the range $[0,2^{16}-1]$. This operation can be defined as $SHL(c_x,c_n) = c_{(x * 2^n) \mod 2^{16}}$, where $c_x$ and $c_n$ are ciphertexts encrypting the input integer $x$ and the number of shifted bits $n$, respectively, in their first slots. The value of $n$ is constrained between 0 and 16. The output ciphertext should encrypt the logical shifted value $SHL(x,n) = (x * 2^n) \mod 2^{16}$ in its first slot, which is also a value in the range $[0,2^{16}-1]$. 

## Approach

The proposed solution employs a two-way lookup table approach, using $x$ and $n$ as keys and $SHL(x,n)$ as the lookup value. In this way, the computation in the encrypted domain is expressed as:
\begin{equation} SHL(c_x, c_n) = \sum_{i=0}^{2^{16}-1}\left( EQ(c_x, i) \times \sum_{k=0}^{15} EQ(c_n, k) \times SHL(i, k) \right), \end{equation}
where
\begin{equation}
    EQ(a,b) = 
    \begin{array}{rl}
        1 & \text{if } a = b \\
        0 & \text{if } a \neq b 
    \end{array}
\end{equation}
is the equality function. Notably, the term for $k=16$ is omitted since the computation naturally returns $0$ when $n=16$, which is the correct result.

$$
f(x)=
\begin{cases}
1/d_{ij} & \quad \text{when $d_{ij} \leq 160$}\\ 
0 & \quad \text{otherwise}
\end{cases}
$$

To optimize the number of comparisons, we leverage the SIMD property of the underlying BFV/BGV system by transforming the above equation to:
$$
\text{SHL}(c_x,c_n) = \text{SumSlots} \left( 
  \text{EQ}\left( \text{Duplicate}(c_x), p^{\text{in}} \right) 
  \cdot \sum_{k=0}^{16} \text{EQ} \left( \text{Duplicate}(c_n), k \right) 
  \cdot p^{\text{out}}_k 
\right)
$$


Here the $Duplicate(.)$ function function replicates the value in the first slot of a ciphertext across its first $2^{16}$ slots, while the $SumSlots(.)$ function sums the first $2^{16}$ slots of a ciphertext, placing the result in the first slot. These functions can be implemented using sequencial rotation and addition operations. Additionally, $p^\text{in}$ is the plaintext that encodes the vector $[0,1,\dots,2^{16}-1]$ containing all possible input values, and $p^\text{out}_k$ encodes the vector $[SHL(0,k),SHL(1,k),\dots,SHL(2^{16}-1,k)]$ for all possible output values given the shifted amount $k$.

By precompute the plaintexts $p^\text{out}_k$ for all possible $k$ values, the remaining task is to implement the equality comparison function between a ciphertext and a plaintext value. Due to different ranges of $x$ and $n$, two distinct equality comparison methods are employed for optimal performance. Specifically, Fermat's Little Theorem (FLT) is used for comparing values in $Duplicate(c_x)$ and $p^\text{in}$ (referred to as the outer comparison), while the Lagrange polynomial method is used for comparing $Duplicate(c_n)$ and $k$ (referred to as the inner comparison).

### Outer Equality Comparison

The FLT method is utilized to evaluate $ \text{EQ}\left(\text{Duplicate}(c_x),p^\text{in}\right) $. This function returns a ciphertext where the $i$-th slot is one if $i$ equals $x$ and zero otherwise. This approach is similar to the FHERMA's Lookup Table solution [1]. However, given the input range $[0,2^{16}-1]$, the plaintext modulus $Q$ must be set higher, specifically $Q=786433=3\times2^{18}+1$, to encode the values correctly. To begin with, we subtract $p^\text{in}$ from $\text{Duplicate}(c_x)$. The resulting ciphertext $c_\text{diff} = (\text{Duplicate}(c_x)-p^\text{in})$ contains exactly one zero at the $x$-th slot and non-zero values in other slots. We then compute the exponentiation $c_\text{diff}^{3\times2^{18}} = c_\text{diff}^{2^{19}}\times c_\text{diff}^{2^{18}}$, which consumes 20 multiplication levels in total. The final comparison results is obtained by evaluating $1 - c_\text{diff}^{3\times2^{18}}$.

### Inner Equality Comparison

For a fixed value of $k$ ($0\leq k \leq 15$), the function $EQ\left(Duplicate(\mathtt{c}_n),k\right)$ can be represented by a Lagrange polynomial with integer coefficients $p(z)$, calculated over the interpolation nodes $0,1,\dots,16$ and the corresponding values $p(z) = 1$ at $z=k$ and $0$ elsewhere. The coefficients of $p(n)$ are computed by using modular multiplication and division in the plaintext modulus $Q$. As the degree of $p$ is 17, its evaluation consumes 5 multiplication levels using the Paterson-Stockmeyer algorithm. We modified the `EvalPolyPS` from the OpenFHE library to accommodate integer coefficient polynomials.

However, the above approach requires 16 executions of the Paterson-Stockmeyer algorithm, which can be time-consuming. This can be reduced to a single execution in a SIMD fashion. Similar to the outer comparison, we calculate the subtraction $(Duplicate(\mathtt{c}_n) - \mathtt{p}^\text{shift})$, where $\mathtt{p}^\text{shift}$ encodes the vector $[0,1,\dots,15]$ of possible $k$ values. We then compute a Lagrange polynomial $p(.)$ at the interpolation nodes $-16,-15,\dots,0,\dots,15,16$, where the polynomial value is $1$ at zero and $0$ elsewhere. In this way, the transformed ciphertext $p\left( Duplicate(\mathtt{c}_n) - \mathtt{p}^\text{shift}\right)$ is equivalent to $EQ\left(Duplicate(\mathtt{c}_n),\mathtt{p}^\text{shift}\right)$, having a $1$ at the $n$-th slot and $0$ elsewhere. Finally, $EQ\left(Duplicate(\mathtt{c}_n),k\right)$ can be derived from $EQ\left(Duplicate(\mathtt{c}_n),\mathtt{p}^\text{shift}\right)$ for different $k$ values by by applying a mask to extract the $k$-th slot and duplicating it across the first $2^{16}$ slots. This requires only one multiplication and some rotations, without further polynomial evaluation.

### Extra Level Reduction

After evaluating $\text{EQ}\left(\text{Duplicate}(c_x),p^\text{in}\right) = 1 - c_\text{diff}^{3\times2^{18}}$ and the summation of inner comparisons

$ \sum_{k=0}^{16} \text{EQ}(\text{Duplicate}(c_n), k) \cdot p^{\text{out}}_k = c_{\text{sum}} $
, these results must be multiplied together, which incurs an additional level of computation. To avoid this, the multiplication order can be rearranged as

$ c_\text{sum} - c_\text{diff}^{2^{19}} \times\left(c_\text{diff}^{2^{18}} \times c_\text{sum}\right) $
, thus maintaining the total computation depth at 20.


## References

[1] **Lookup Table Challenge** https://fherma.io/content/66d9c84af6ea18c58bf5e97a
