# Max Element Search over an Encrypted Vector

*The article details the solution provided by the winner of the [Max Element challenge](https://fherma.io/challenges/6661824ecf10b677de4e0cf6/overview).*

**Author:** Vivian Maloney, cryptography researcher at the Johns Hopkins University Applied Physics Laboratory

## Introduction
We are tasked with finding the maximum value in an encrypted array of length $n=2048$, where each entry is an integer within [0, 256). This solution is implemented using BFV homomorphic encryption, taking advantage of the discrete nature of the values and FHE’s SIMD parallelism.

### The Path Not Taken
In traditional, unencrypted computation, a binary tree of pairwise comparisons can find the maximum element with $n \log_2(n)$ comparisons and a circuit depth of $O(\log_2(n))$. However, this approach does not map well to FHE, given its depth constraints and the benefits of parallelism in SIMD operations.


## Algorithm Overview

### Step Polynomial Evaluation
We evaluate whether each element of the encrypted array is greater than or equal to a threshold $i$, using a step polynomial:

$$
f_i(x) = 
    \begin{cases} 
        1 & \text{if } x \geq i \\
        0 & \text{otherwise}
    \end{cases}
$$

This step is computed for every threshold $i$ between 1 and $m = 256$.

### Algorithm Pseudocode
The algorithm we implemented corresponds to the following pseudocode:
```python
def max(x, m=256):
    sum = 0
    for i in range(1, m):
        y = (x >= i)
        if np.any(y):
            sum += 1
    return sum
```
For each threshold $i$, we perform two key operations:
1. **Elementwise Comparison**: Compare each encrypted value with $i$ to get a binary result (1 if $x_j \geq i$, 0 otherwise).
2. **Boolean Aggregation**: Use a homomorphic NAND operation to check if any element in the array exceeds $i$.

## Boolean Aggregation via NAND
The NAND operation checks whether any element of the array exceeds the threshold $i$. The homomorphic NAND function is implemented as follows:
```python
def NAND(y, n):
    z = 1 - y
    r = 1
    while r < n:
        z = z * (z << r)
        r *= 2
    z = 1 - z
    return z
```
This approach reduces the multiplicative depth during iterations, making later steps faster.

## FHE Comparison

In FHE, non-linear operations like comparisons are evaluated using polynomials. For each threshold $i$, we use Lagrange interpolation to construct a polynomial that acts as a step function:
$$
f_i(x) = \begin{cases} 
1 & \text{if } x \geq i \\
0 & \text{otherwise}
\end{cases}
$$
An alternative approach involves subtracting the threshold $i$ from each element and applying a unary Heaviside step function, defined as:
$$
H(y) = \begin{cases} 
1 & \text{if } y \geq 0 \\
0 & \text{otherwise}
\end{cases}
$$
This results in a polynomial evaluation over the expanded range $(-m, m)$ instead of $[0, m)$, which simplifies the step function's definition but incurs additional multiplicative depth. The expanded range allows for more straightforward evaluation but trades off efficiency due to the need for deeper circuits.

## Parallelization with SIMD
Since $n = 2048$ is smaller than half the ring dimension (16384), we can duplicate the encrypted array across the available slots and process different thresholds $i$ in parallel. The polynomial coefficients for each threshold are encoded as plaintext vectors, and ciphertext-plaintext multiplications are used to evaluate the different polynomials.

## CKKS Alternative
While our current approach uses BFV for discrete integers, an alternative implementation using CKKS could leverage approximate comparisons. A well-known method for comparing encrypted numbers in CKKS relies on Chebyshev polynomials to approximate the absolute value function, allowing us to compute:
$$
\text{max}(x, y) = 0.5 \times (x + y + |x - y|)
$$
Since the array values are discrete, the Chebyshev approximation of the absolute value function only needs to be accurate within the small range of noise.

This approach can yield more efficient results than the method described in the paper *Numerical Method for Comparison on Homomorphically Encrypted Numbers* by Jung Hee Cheon et al. ([Cheon et al., 2019](https://eprint.iacr.org/2019/417)).

## Conclusion
This approach efficiently computes the maximum in an encrypted array by combining polynomial step functions, NAND-based Boolean aggregation, and SIMD parallelism. The result is an optimized homomorphic computation suitable for BFV.