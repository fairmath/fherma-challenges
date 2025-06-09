# SIGN Function under FHE #

*The article details the solution provided by the winner of the [Sign Evaluation challenge](https://fherma.io/challenges/652bf668485c878710fd020a/overview).*

**Author:** [Aikata](https://www.iaik.tugraz.at/person/aikata-aikata/), Ph.D. student at TU Graz

The sign function, also known as signum, determines the sign of a value. It has significant applications in machine learning, serving as a foundational element for non-linear activation functions like the Rectified Linear Unit (ReLU) or Max Pooling. This is attributed to the ability of the sign function to facilitate comparison or max operations in the following manner:

\begin{align}
    \text{comp}(a,b) &= \frac{ \text{sign}(a-b)+1}{2}
\end{align}

\begin{align}
    \text{max}(a,b) &= \frac{ (a+b)+(a-b) \text{sign}(a-b)}{2}
\end{align}

Fully Homomorphic Encryption (FHE) schemes like FHEW or TFHE can precisely compute the sign function using bootstrapping-based function evaluation, resembling a look-up table. However, in approximate or integer arithmetic schemes like CKKS, BGV, BFV, etc., the absence of table look-up capabilities makes evaluating non-polynomial discontinuous functions challenging. Consequently, these schemes resort to function approximation for sign evaluation. For example, **Figure 1 (a)** demonstrates the effective use of Tanh with a modified domain (e.g., $x, 2\times x, \cdots, 128\times x$) to approximate the sign function. This helps bridge the discontinuity of the sign function using a continuous function. Note that Tanh is not a polynomial function, hence, a polynomial approximation of Tanh, such as the Taylor series, will be applied to approximate the sign function.


|![Sign_plot](https://hackmd.io/_uploads/H1mcK48h6.png)|![cheb_approx](https://hackmd.io/_uploads/Bkj5FNI3T.png)|
:-------------------------:|:-------------------------:
|*a) Signum function approximation using Tanh series (64,128).*| *b) Signum function approximation using Chebyshev series (8,16).*|

**Figure 1:** Function approximations for the sigmoid function.

In recent years, significant progress has been made in the field of FHE, leading researchers to explore methods for effectively approximating the sign function. One prevalent approach involves leveraging the Chebyshev series, known for its universal applicability in approximating a broad spectrum of functions. Notably, OpenFHE has already incorporated an implementation of the Chebyshev series. This implementation evaluates the Homomorphic modular reduction during the Bootstrapping procedure.

The challenge has test cases with values $\in [-1,1]$ and allowed multiplicative depth of 10.

An optimization of the sign approximation technique was introduced in [this paper](https://eprint.iacr.org/2020/834). In this research, the authors advocate for a sign approximation approach based on polynomial composition, with Chebyshev as the basis polynomial. They suggest and validate the effectiveness of dividing the computation depth, denoted as $d$, into smaller segments (e.g., $d_1d_2$ where $d_1+d_2=d$). The proposed methodology initially evaluates a function that approximates the Chebyshev series for depth $d_1$. The obtained result is then utilized as an input for the Chebyshev series of depth $d_2$. This approach could not be utilized to achieve high accuracy required by FHERMA challenge.

Initially, employing a straightforward approximation of the sign function through the Chebyshev series evaluation within the OpenFHE library yields an accuracy of **99.96%**. It is important to note that the Chebyshev series can only be evaluated up to the coefficient $1006$ when approximating $\text{Tanh}(x\times\texttt{RANDMAX})$ using OpenFHE. The resulting approximation is illustrated in **Figure 1(b)**. To enhance the computational capabilities of OpenFHE, we conducted an analysis to determine the feasibility of evaluating additional Chebyshev series. Since the sign function is an odd function, the even degree coefficients do not contribute to its approximation. Hence, there is no need to evaluate the even terms of the Chebyshev series.

Building on this observation, we explored whether it is possible to evaluate $c \times\textbf{T}_{1009}$ while adhering to the multiplicative depth limitation of 10, where $c$ is the coefficient resulting from the function approximation. We utilize the properties of the Chebyshev series and write down recursive relations as follows:

\begin{align}
    \text{c}\times T_{1009} && \rightarrow && \text{2c}\times T_{512}\times T_{497}-\text{c}\times T_{15} && \rightarrow &&   T_{512}\times(\text{2c}\times T_{497})-\text{c}\times T_{15}
\end{align}

\begin{align}
    \text{2c}\times T_{497} && \rightarrow &&  \text{4c}\times T_{256}\times T_{241}-\text{2c}\times T_{15} && \rightarrow  &&  T_{256}\times(\text{4c}\times T_{241})-\text{2c}\times T_{15}
\end{align}

\begin{align}
    \text{4c}\times T_{241} && \rightarrow  && \text{8c}\times T_{128}\times T_{113}-\text{4c}\times T_{15} && \rightarrow &&   T_{128}\times(\text{8c}\times T_{113})-\text{4c}\times T_{15}
\end{align}

\begin{align}
    \text{8c}\times T_{113} && \rightarrow &&  \text{16c}\times T_{64}\times T_{49}-\text{8c}\times T_{15} && \rightarrow &&   T_{64}\times(\text{16c}\times T_{49})-\text{8c}\times T_{15}
\end{align}

\begin{align}
    \text{16c}\times T_{49} && \rightarrow &&  \text{32c}\times T_{32}\times T_{17}-\text{16c}\times T_{15} && \rightarrow &&   T_{32}\times(\text{32c}\times T_{17})-\text{16c}\times T_{15}
\end{align}

\begin{align}
    \text{32c}\times T_{17} && \rightarrow &&  \text{64c}\times T_{16}\times T_{1}-\text{32c}\times T_{15} && \rightarrow &&   T_{16}\times(\text{64c}\times T_{1})-\text{32c}\times T_{15}
\end{align}

Upon the initial breakdown of $\textbf T_{1009}$, we observed that the series terms to be multiplied ($\textbf T_{512}$, $\textbf T_{497}$) were at the same depth of 9. Unfortunately, this configuration made it impossible to perform a third multiplication with the coefficient $\text{c}$. Therefore, we recursively broke down the expression until we achieved terms ($\textbf T_{16}$, $\textbf T_{1}$) at different depths (4,1). At this stage, we can multiply $\text{c}$ with $\textbf T_{1}$, bringing it to a depth of 1. Subsequently, we can compute the recursive breakdown upwards to obtain $c \times \textbf T_{1009}$. This strategy allows to evaluate more Chebyshev series coefficients effectively.

The same methodology is applied to evaluate all the remaining Chebyshev series coefficients - $\textbf T_{1011}$, $\textbf T_{1013}$, $\textbf T_{1015}$, $\textbf T_{1017}$, $\textbf T_{1019}$, $\textbf T_{1021}$, and $\textbf T_{1023}$. The recursion must be further broken down to evaluate higher degree coefficients. This additional evaluation increases accuracy from **99.96%** to **99.97%**. The approximation for this is shown in the **Figure 1 (b)**.

The newfound capability to evaluate the full depth presents an intriguing opportunity to explore potential improvements or attempt to reproduce the results outlined in [this paper](https://eprint.iacr.org/2020/834). This increased depth computation also serves to improve the efficiency of other function approximations, for example, the logistic function.