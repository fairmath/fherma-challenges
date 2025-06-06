# ReLU Function under FHE

*The article details the solution provided by the winners of the [ReLU Function challenge](https://fherma.io/challenges/6542c282100761da3b545c3e/overview).*

**Authors:** [Janis Adamek](https://rcs.mb.tu-dortmund.de/about-us/team/researchers/janis-adamek/), [Dieter Teichrib](https://rcs.mb.tu-dortmund.de/about-us/team/researchers/dieter-teichrib/), [Philipp Binfet](https://rcs.mb.tu-dortmund.de/about-us/team/researchers/philipp-binfet/), and [Moritz Schulze Darup](https://rcs.mb.tu-dortmund.de/about-us/team/heads/moritz-schulze-darup/) from Control and Cyberphysical Systems Group, TU Dortmund, Germany.

## Introduction

The rectified linear unit (ReLU) is commonly used as a nonlinear activation function in neural networks (NN). An encrypted implementation of such NN can, e.g., be realized by substituting the ReLU activation with polynomial approximations. In this context, the common limitation to a fixed multiplicative depth often requires polynomial approximations of low or moderate order. For instance, the multiplicative depth for this particular challenge was limited by $29$ for **Testcase #1** and by $4$ for **Testcase #2**. Now, it is well known in the literature (see [1]) that a multiplicative depth of $d \in \mathbb{N}$ enables the implementation of polynomials of order $n=2^d-1$ in an encrypted fashion.

## Testcase #1

For $d=29$ as in **Testcase #1**, $2^d-1$ evaluates to $536870911$. Thus, since very high orders are supported, it has been straightforward to fit a polynomial approximating the ReLU in such a way that $100$% accuracy is achieved for the encrypted samples in the interval $[-1,1]$. In fact, we simply used OpenFHE's built-in Chebyshev approximation of order $n=1000$. The nearly perfect fit is illustrated in **Figure 1**.

![Figure 1: ReLU approximation using a Chebyshev polynomial of order 1000](https://d2lkyury6zu01n.cloudfront.net/images/blog/p_d1000.png)

***Figure 1**: ReLU approximation using a Chebyshev polynomial of order 1000.*

## Testcase #2

Obtaining a decent result for **Testcase #2** with $d=4$ has been significantly more challenging. In fact, a standard Chebyshev approximation of order $n=2^d-1=15$ (see **Figure 2** for the illustration) here resulted in an accuracy of only $63$%.

![Figure 2: (left) ReLU approximation using a Chebyshev polynomial of order 15. (right) Chebyshev approximation with error threshold](https://d2lkyury6zu01n.cloudfront.net/images/blog/p_d15_combined.png)

***Figure 2**: (left) ReLU approximation using a Chebyshev polynomial of order 15. (right) Chebyshev approximation with error threshold.*

We improved this result by applying the following two tricks. First, we formulated a regression problem, which explicitly took the requirements for the challenge into account. More precisely, we considered a regular grid of sample points $x_i \in [-1,1]$ and searched for a polynomial $p(x)$, which is such that the number of outliers $p(x_i) \notin [-\epsilon,\epsilon]$ is minimal, where the tolerance $\epsilon = 10^{-3}$ has been specified in the task.

Second, we found a way to extend the maximum implementable order to $n=2^d$ given that the leading coefficient $a_n$ of the polynomial is integer. In fact, in this special case, we can avoid the multiplication $a_n x^n$ (which would have otherwise consumed one level of the available multiplicative depth) and compute the sum $x^n + \dots + x^n$ with $|a_n|$ summands using "cheap" encrypted additions (or subtractions). Both tricks, i.e., minimizing the number of outliers and considering an integer lead coefficient can be implemented using mixed-integer (MI) programming. More precisely, we formulated the design problem as an MI linear program (MILP) and solved it using **MOSEK** [2]. The resulting polynomial is

$$
\begin{align*}
p(x)&=0.0324+0.5x+2.1348x^2-13.9209x^4+70.0983x^6-213.0967x^8+385.9436x^{10}\\
\end{align*}
$$$$
\begin{align*}
&-407.0473x^{12}+230.3549x^{14}-54x^{16}
\end{align*}
$$

and it is illustrated in **Figure 3**. The achieved accuracy on **Testcase #2** is $88.4$%.

![Figure 3: (left) Approximation of the ReLU function with a polynomial of order 16. (right) Polynomial approximation with error threshold](https://d2lkyury6zu01n.cloudfront.net/images/blog/p_d16_combined.png)

***Figure 3**: (left) Approximation of the ReLU function with a polynomial of order 16. (right) Polynomial approximation with error threshold.*

## References

[1] **Eunsang Lee, Joon-Woo Lee, Jong-Seon No, and Young-Sik Kim**. Minimax approximation of sign function by composite polynomial for homomorphic comparison. IEEE Transactions on Dependable and Secure Computing, 19(6):3711–3727, 2022. Preprint available online at https://eprint.iacr.org/2020/834

[2] **MOSEK ApS**. The MOSEK optimization toolbox for MATLAB manual. Version 10.0, 2024. https://docs.mosek.com/10.0/toolbox/index.html.
