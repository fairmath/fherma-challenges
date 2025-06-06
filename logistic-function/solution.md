# Logistic (Sigmoid) Function under FHE #

*The article details the solution provided by the winner of the [Logistic Function challenge](https://fherma.io/challenges/652bf648485c878710fd0208/overview).*

#### Author: [Aikata, Ph.D. student at TU Graz](https://www.iaik.tugraz.at/person/aikata-aikata/)

## Introduction

The logistic (a.k.a., sigmoid) function forms the basis for logistic regression-based machine learning. It is commonly employed as a non-linear activation function in neural networks. Homomorphic schemes like CKKS only support polynomial arithmetic operations, and expressing the sigmoid function as a polynomial is not feasible. Various series, such as the Taylor series or the Chebyshev series, are utilized to approximate the sigmoid function. Recent efforts have focused on developing privacy-preserving models for logistic regression training and inference by employing similar approximations of the logistic function - works [1](http://eprint.iacr.org/2018/254), [2](http://eprint.iacr.org/2018/074), [3](http://arxiv.org/abs/1611.01170), and [4](https://doi.org/10.1145/2857705.2857731). Therefore, it is crucial to investigate the extent to which we can approximate the logistic function under constrained multiplicative depth.

## Sigmoid Approximation

The challenge contains two sets of test cases, distinguished solely in terms of the permitted multiplicative depth. The input values for both sets of test cases are confined to the range of $[-25, 25]$. The straightforward logistic evaluation of this range is illustrated in Figure 1.

| ![sigmoid_2](https://hackmd.io/_uploads/BkdAYe83a.png) | ![sigmoid_1](https://hackmd.io/_uploads/HkT6FgLhp.png) |
|:------------------------------------------------------:|:------------------------------------------------------:|
| *a) Sigmoid and its function approximation using Chebyshev series (64,128).* | *b) Sigmoid and its function approximation using Chebyshev series (8,16).* |

**Figure 1:** Sigmoid function and its approximation using Chebyshev series.

As previously mentioned, one common method for approximating the logistic function involves employing the Chebyshev series. However, the Chebyshev series provides results over the domain [−1, 1]. To apply the Chebyshev series to broader ranges (e.g., $[a,b]$), the input polynomial (e.g., $x$) is scaled to bring it to the interval $[-1,1]$ as outlined below, ensuring the applicability of the Chebyshev approximation.

\begin{align}
x' & = \frac{2x - (b+a)}{b-a}
\end{align}

\begin{align}
x' & = \frac{x}{\omega}
\end{align}

\begin{align}
\text{ when } |a|=|b|, a \neq b,\text{ and }\omega=|b|
\end{align}

The scaled ciphertext $x'$ is subsequently employed for the approximation. However, note that this scaling results in the loss of one multiplicative depth. This aspect is explicitly mentioned in the [library documentation](https://github.com/openfheorg/openfhe-development/blob/main/src/pke/examples/FUNCTION_EVALUATION.md) for function evaluation.

Consequently, when presented with a challenge specifying a multiplicative depth $d$ over an arbitrary range $[a,b]$, such that $a\\neq-1$ and $b\\neq1$, the available Chebyshev series approximation technique allows us to evaluate up to a depth of $d-1$ at best. To fully exploit this using OpenFHE, the technique described in the [SIGN challenge solution](https://fherma.io/content/65de3f45bfa5f4ea4471701c) can be applied. However, it becomes evident that although reducing the depth from 7 to 6 $(2^7=128 \\rightarrow 2^6=64)$, as shown in Figure 1(a) does not result in a significant loss of accuracy, but dropping from 4 to 3 ($2^4 = 16 \\rightarrow 2^3 = 8$) entails a considerable loss (Figure 1(b)). Therefore, our exploration focuses on enhancing this existing technique to yield the best approximation results.

## Test case #1

The first test case permits a multiplicative depth of 7. Initially, let's assess the capabilities of the current implementation to determine how well we can approximate. With OpenFHE's ChebyshevPS implementation, we find that we can evaluate the Chebyshev series up to the coefficient 59. Applying the SIGN challenge strategy can extend this evaluation to 63 coefficients, resulting in an impressive accuracy of 99.99%. To walk the extra mile (or 0.01%) for achieving complete accuracy, let's delve into the recursive unroll of $T_{65}$ as outlined below:

\begin{align}
    \text{c}\times T_{65} && \rightarrow && \text{2c}\times T_{32}\times T_{33}-\text{c}\times T_{1} && \rightarrow &&  T_{32}\times(\text{2c}\times T_{33})-\text{c}\times T_{1} 
\end{align}

\begin{align}
    \text{2c}\times T_{33} && \rightarrow &&  \text{4c}\times T_{16}\times T_{17}-\text{2c}\times T_{1} && \rightarrow  && T_{16}\times(\text{4c}\times T_{17})-\text{2c}\times T_{1}
\end{align}

\begin{align}
    \text{4c}\times T_{17} && \rightarrow  && \text{8c}\times T_{8}\times T_{9}-\text{4c}\times T_{1} && \rightarrow &&  T_{8}\times(\text{8c}\times T_{9})-\text{4c}\times T_{1}
\end{align}

\begin{align}
    \text{8c}\times T_{9} && \rightarrow &&  \text{16c}\times T_{4}\times T_{5}-\text{8c}\times T_{1} && \rightarrow &&  T_{4}\times(\text{16c}\times T_{5})-\text{8c}\times T_{1}
\end{align}

\begin{align}
    \text{16c}\times T_{5} && \rightarrow &&  \text{32c}\times T_{2}\times T_{3}-\text{16c}\times T_{1} && \rightarrow &&  T_{2}\times(\text{32c}\times T_{3})-\text{16c}\times T_{1}
\end{align}

Note that this recursive breakdown is just one of the numerous possible approaches. Examining this breakdown, we notice that at each step the two coefficients to be multiplied are at different depths, and one consistently exceeds the exploitable multiplicative depth at that level. Thus, let's continue the breakdown until we reach $T_2$ and $T_3$, which can be represented as follows:

\begin{align}
    T_{2} && \rightarrow && \text{2x}'^2-1 && \text{// Multiplicative depth 2}
\end{align}

\begin{align}
    c\times T_{3} && \rightarrow && \text{4cx}'^3-\text{3cx}'  && \text{// Multiplicative depth 3}
\end{align}

Keep in mind that $T_3$ is at a higher depth compared to $T_2$. The computation of $T_{65}$ relies on our ability to compute $32c\times T_3$ while remaining at the same multiplicative depth as $T_2$. In this context, we emphasize that *the sky is not the limit* and indeed, there is a method to accomplish this, as illustrated in the equations below:

\begin{align}
     32c\times T_3 && \rightarrow && \frac{128c}{\omega^3} x^3-\text{96cx}'  && \text{// Multiplicative depth 2}
\end{align}

\begin{align}
    && && && \rightarrow && (\frac{128c}{\omega^3}x)(x^2)-\text{96cx}'  && \text{// Multiplicative depth 2}
\end{align}

The logistic function is an odd function, and only the odd coefficients of the Chebyshev series contribute to its approximation. Leveraging recursive breakdowns like the one for $T_{65}$, we calculate odd series coefficients up to $T_{77}$, almost achieving our target of a 100% (99.9988%) accuracy for this particular test case. While approximating up to $T_{77}$ sufficed for the first test case, it remains to investigate how far we can extend this breakdown before reaching limitations.

## Test case #2

In this particular test case, a multiplicative depth of 4 is mandated. The straightforward Chebyshev series computation up to coefficient 7 resulted in an accuracy of 88.12%, falling short of the minimum requirement of 90%. Therefore, a comprehensive exploration of the approach identified in the previous test case becomes necessary. It is important to highlight that Chebyshev series computation can be transformed into a simple polynomial evaluation. Given the low multiplicative depth, it becomes evident that converting the Chebyshev computation to polynomial evaluation is crucial for a thorough investigation of the limitations of the aforementioned technique.

An example of coefficients generated for evaluating an unscaled polynomial of degree 16 are as follows: `{0.5, 0.19, 0.0, -0.004, 0.0, 4.83e-05, 0.0, -2.97e-07, 0.0, 1.02e-09, 0.0, -1.94e-12, 0.0, 1.94e-15, 0.0, -7.89e-19, 0.0}`. Notably, the values of these coefficients decrease progressively. This diminishing trend arises because the scaling factor, previously managed by the ciphertext, is now concentrated at the coefficient level. We compute the evaluation up to $x^7$ in a very straightforward manner, as shown below

\begin{align}
     \texttt{SUM}_7 = (c_7\times x^4)\times x^3 +(c_5\times x^3)\times x^2 +(c_3\times x^2)\times x + c_1\times x+ c_0 
\end{align}

For the next evaluation, it is apparent that coefficients 9, 11, 13, and 15 are exceedingly small, nearly reaching the limits of the scaling factor. It will result in computational errors if not handled cautiously. Hence, we recommend breaking down the computation of higher coefficients into smaller chunks, as outlined below:

\begin{align}
    y_1 && = && (10^{-3}\times x )\times x && \text{// $10^{-3}\times x^2$ at depth 2}
\end{align}

\begin{align}
    y_2 && = && (c_9\times 10^{6} \times x )\times x && \text{// $c_9 \times 10^{6}\times x^2$ at depth 2}
\end{align}

\begin{align}
    c_9\times x^9 && = && (y_1\times y_1) \times (y_2\times x^3) &&
\end{align}

Applying this approach, we can extend the evaluation up to $x^{13}$ as depicted in the equation below. This limitation arises because the coefficient computation needs to be divided into at least two parts. The maximum degree achievable with two constant multiplications in this manner is $x^{14}$. Thus, we have reached the limit of this technique.

\begin{align}
    y_1 && = && (10^{-6}\times x )\times x^2 && \text{//$10^{-6}\times x^3$ at depth 2}
\end{align}

\begin{align}
    y_2 && = && (c_{13}\times 10^{12} \times x )\times x^2 && \text{// $c_{13} \times 10^{12}\times x^3$ at depth 2}
\end{align}

\begin{align}
    c_{13}\times x^{13} && = && (y_1\times y_1) \times (y_2\times x^4) &&
\end{align}

The computation up to $x^{13}$ led to an enhancement in accuracy from 88.12% to 96.6%, which is a significant improvement in the attainable accuracy. Exploring the effectiveness of this approach in other approximating functions at different depths seems to be an interesting area for future investigation.
