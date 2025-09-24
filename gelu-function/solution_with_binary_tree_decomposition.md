# GELU Approximation in FHE with a Binary-Tree Product Decomposition Strategy

*The article details the solution provided by the winner of the [GELU Function challenge](https://fherma.io/challenges/683eaf48eed44a699f640a92).*

**Author:** [Chi-Hieu Nguyen](https://www.linkedin.com/in/hieu-nguyen-ba6548316), University of Technology Sydney, Australia.

## Introduction

The challenge requires implementing the GeLU activation function, widely used in deep learning, under homomorphic encryption. According to the challenge description, input data are sampled from the domain $[-7,7]$ following a normal distribution. Accuracy is evaluated by counting the number of slots in the output vector where the absolute error is below $0.001$.

## Polynomial Approximation

We adopt a minimax approximation, e.g., using Remez algorithm, to approximate the GeLU function over the target domain, ensuring 100% accuracy across the entire range. By progressively increasing the polynomial degree, we determine that degree 22 is the minimum required to satisfy the error threshold, achieving a maximum error of $4.4 \times 10^{-4}$. **Figure 1** illustrates the degree-22 polynomial approximation and the corresponding absolute error. The coefficients, expressed in the Chebyshev basis, are as follows
```
p = [2.205108264359930015e+00, 3.499999999999999556e+00, 1.528721347815146681e+00, -1.647976405698982102e-15, -3.325936224062873703e-01, 1.437489594390790025e-15, 1.521190036383314459e-01, -8.453684227375073390e-16, -8.430346518496759090e-02, -1.673523292483670998e-15, 4.886015896854042917e-02, 2.863693178149025070e-15, -2.791811221502403864e-02, -1.859411993163826857e-15, 1.532346888698131633e-02, -5.949712581611852003e-16, -7.993026213095437427e-03, -1.551375849918958677e-15, 3.952491617355435687e-03, -1.336721660511636056e-16, -1.857562051847814338e-03, 3.326019639171002269e-15, 1.023308862034017419e-03]
```

![gelu](https://hackmd.io/_uploads/r1dadCS5gx.png)
***Figure 1**: (Top) Degree-22 polynomial approximation of the GeLU function. (Bottom) Absolute approximation error across the domain.*


## Polynomial Evaluation

An important observation is that $,\text{GELU}(x) - \tfrac{x}{2},$ is an even function. Consequently, all odd coefficients of the approximated polynomial $p(x)$ are negligibly small, except for the coefficient of $x$, as reflected in the coefficients above. Leveraging this property, we can accelerate evaluation under HE by computing the second Chebyshev polynomial $T_2(x) = 2x^2 - 1$ and then expressing the polynomial as $p_{even}(T_2(x))+c_1x = p(x)$, where $p_{even}$ is a degree-11 polynomial obtained from the even coefficients of $p$. This reduces the effective polynomial degree from 22 to 11, thereby significantly lowering evaluation time.

To evaluate $p_{even}$, one can use the default Paterson–Stockmeyer (PS) algorithm in OpenFHE. Instead, we introduce a binary-tree product decomposition strategy that preserves the ciphertext–ciphertext (CC) multiplication complexity while providing substantially greater parallelism. In this method, we first convert $p_{even}$ to the monomial basis, obtained as follows
```
p_even = [0.00044269650031170116, 0.39574328076312115, -0.0629733653564327, 0.008364135635608984, -0.0007825494992434453, 5.1058610337019434e-05, -2.315976838992098e-06, 7.235122296125314e-08, -1.5214882476900954e-09, 2.0523115610681066e-11, -1.6012937509370233e-13, 5.488829795459728e-16]
```

In this form, the target polynomial is evaluated as  

$$
p(x) = p_{\text{even}}(x^2) + c_1 x .
$$

Let $c_{11}$ denote the leading coefficient of $p_{\text{even}}$, i.e., the coefficient of $x^{11}$ in $p_{\text{even}}(x)$ (equivalently, the coefficient of $x^{22}$ in $p(x)$).  
We normalize this coefficient to unity by rewriting  

$$
p_{\text{even}}(x^2)
= \tilde{p}_{\text{even}}\left(\left(\frac{x}{c_{11}^{1/22}}\right)^2\right),
$$

where the coefficients of the normalized polynomial $\tilde{p}_{\text{even}}$ are given by  

$$
\tilde{c}_i = \frac{c_i}{c_{11}^{i/11}}, \quad i=0,1,\dots,11 .
$$


The resulting coefficients are:
```
p_tilde_even = [0.00044269650031170116, 9.654584128641837, -37.479772490316186, 121.44541723640373, -277.1991560769019, 441.23412948943434, -488.2635908159109, 372.12258290089426, -190.91004230296397, 62.82369627660221, -11.95834898654424, 1.0000000000000009]
```

This transformation ensures that the leading coefficient is normalized to one. Next, $\tilde{p}_{even}$ is factored into five quadratic polynomials and one linear polynomial:

$
\tilde{p}_{even}(x) = (x^2+b_1x+a_1)\dots(x^2+b_5x+a_5)(x+a_6)
$

Each of these six factor polynomials is computed concurrently using OpenMP. The corresponding C++ implementation is shown below:
```cpp
// Scale input x by c_{11}^(1/22) = (5.488829795459728e-16)^(1/22)
auto x = m_cc->EvalMult(m_InputC, 0.20246035278443494);
x = m_cc->EvalSquare(x);
auto x_square = m_cc->EvalSquare(x);

// Define factor coefficients
std::vector<double> A = {5.569522767147481, 4.210402755985315, 0.19986968808436417, 0.8830278939922745, 2.333178076905341, 4.584534226472708e-05};
std::vector<double> B = {-4.6890748970212295, -3.8468619742495944, 0.006438840954910282, -0.9788392119088897, -2.4500575896613714};

#pragma omp parallel for
for (int i = 0; i < 6; i++) {
    if (i == 5) {
        // Compute (x + a_6)
        C[i] = m_cc->EvalAdd(x, A[i]);
        m_cc->GetScheme()->LevelReduceInternalInPlace(C[i], 2);
    } else {
        // Compute (x^2 + b_i x + a_i)
        C[i] = m_cc->EvalMult(x, B[i]);
        C[i] = m_cc->EvalAdd(C[i], A[i]);
        m_cc->EvalAddInPlace(C[i], x_square);
    }
}
```

Notably, $x^2$ is computed only once and reused across factors, requiring only a single CC multiplication for all six factor polynomials.

The factors are then combined using binary-tree multiplication in a depth-optimal manner:

$$
\begin{align}
\tilde{p}_{even}^{1,2}(x) &= (cx^2+b_1x+a_1)(cx^2+b_2x+a_2), \\
\tilde{p}_{even}^{3,4}(x) &= (cx^2+b_3x+a_3)(cx^2+b_4x+a_4), \\
\tilde{p}_{even}^{5,6}(x) &= (cx^2+b_5x+a_5)(x+a_6), \\
\tilde{p}_{even}^{3,4,5,6}(x) &= \tilde{p}_{even}^{3,4}(x) \tilde{p}_{even}^{5,6}(x), \\
\tilde{p}_{even}(x) &= \tilde{p}_{even}^{1,2}(x) \tilde{p}_{even}^{3,4,5,6}(x)
\end{align}
$$

This procedure requires 5 CC multiplications for the binary-tree stage, resulting in a total of 6 multiplications for the entire polynomial, which is identical to the PS algorithm. Notably, the evaluation of $\tilde{p}_{even}^{1,2}$, $\tilde{p}_{even}^{3,4}$, and $\tilde{p}_{even}^{5,6}$ can also be performed in parallel. This enhanced concurrency results in an approximate 30% performance improvement over the PS approach.