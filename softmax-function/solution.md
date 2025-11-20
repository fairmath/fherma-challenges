# Softmax Function

*The article details the solution provided by the winner of the [Softmax Function challenge](https://fherma.io/challenges/688b3aac8c54bd1ddd394085/overview).*

**Author:** Weiduan Feng, cryptography researcher

## Introduction

The softmax function is often used as the last activation function of a neural network to normalize its output to a probability distribution over predicted output classes. It is also used in the attention mechanism of [transformers](https://arxiv.org/pdf/1706.03762) to convert attention scores into probabilities, guiding how much focus the model places on each input token.

Softmax is defined as follows:

$$
\text{Softmax}(z) = \frac{e^{z_i}}{\sum_{j=1}^{n} e^{z_j}}
$$

Where:

- $z = [z_1, z_2, ..., z_n]$ is the input vector,
- $n$ denotes the size of the input vector (e.g., the number of class logits in classification, vocabulary size in language models, or the number of input sequence tokens in transformers).

The goal of this challenge is to implement an algorithm that evaluates the Softmax function on encrypted data.

## Approximation approach

Our computation consists three steps:

1. Compute the exponential function $e^{z_i}$ on encrypted $z_i$.
2. Sum the exponential results from 1.
3. Invert the sum and multiply it with the exponential results to obtain the final $\text{Softmax}(z)$.

Now we dive into the details.

### 1. Compute the exponential function.

- Input: an encrypted vector $Z = [z_0, z_1, \cdots, z_{n-1}]$ (here $n = 128 = 2^7$ in the challenge).
- Output: an encrypted vector $E = [e^{z_0}, e^{z_1}, \cdots, e^{z_{n-1}}]$.

The exponential function $e^x$ has the power expansion
$$
e^x =\sum_{i=0}^\infty \frac{x^i}{i!} = 1 + \frac{x}{1!} + \frac{x^2}{2!} + \frac{x^3}{3!} + \frac{x^4}{4!} + ...,
$$
which is absolutely convergent for every real value of $x$.

We use the first $K+1$ terms to approximate $e^x$ where $K = 2^N$ for convenience. Let us leave the first term 1 for now,


$$
\begin{array}{rcl}
e^x - 1 &\approx& \frac{x}{1!} + \frac{x^2}{2!} + \frac{x^3}{3!} + \frac{x^K}{K!}\cr
 &=& \frac{x}{1} +\frac{x}{1} \frac{x}{2} + \ldots + \frac{x}{1} \frac{x}{2} \frac{x}{k}\cr
\end{array}
$$
Let $t_i = z/(i+1), i = 0,\ldots, K-1$, i.e.,

$$ \begin{array}{rcl} t_0 &=& [\frac{z_0}{1}, \frac{z_1}{1}, \ldots, \frac{z_{n-1}}{1}]\cr 
t_1 &=& [\frac{z_0}{2}, \frac{z_1}{2}, \ldots, \frac{z_{n-1}}{2}]\cr 
&\cdots&\cr 
t_{K-1} &=& [\frac{z_0}{K}, \frac{z_1}{K}, \ldots, \frac{z_{n-1}}{K}]\cr \end{array} $$

Then (note that $K=2^N$)
$$
\begin{array}{rcl}
e^z - 1 &\approx& t_0 + t_0t_1 + \ldots + t_0t_1\cdots t_{2^N-1}\cr
&=& (t_0 + t_0t_1 + t_0\cdots t_{2^{N-1}-1}) \cr
& & + t_0\cdots t_{2^{N-1}-1}(t_{2^{N-1}} + t_{2^{N-1}}t_{2^{N-1}+1} + \ldots + t_{2^{N-1}}\cdots t_{2^N-1})
\end{array}
$$
which can be computed efficiently by a "divide-and-conquer" algorithm. We use a non-recursive algorithm (Algorithm 1), an example for $K=8$ follows:

$$
\begin{array}{rcl}
&&t_0 + t_0t_1 + \ldots + t_0t_1\cdots t_{7}  \cr
&=& (t_0 + t_0t_1 + t_0t_1t_2 + t_0t_1t_2t_3) + t_0t_1t_2t_3(t_4+t_4t_5 + t_4t_5t_6+t_4t_5t_6t_7)\cr
&=& ((t_0 + t_0t_1) + t_0t_1(t_2 + t_2t_3)) + t_0t_1t_2t_3((t_4+t_4t_5) + t_4t_5(t_6+t_6t_7))
\end{array}
$$

**Algorithm 1**: ExpMinus1  
**In:** $T = [t_0, t_1, \ldots, t_{2^N-1}]$.  
**Out:** $s = \sum_{i=0}^{2^N-1}\prod_{j=0}^i t_j$. 
```text
FOR i = 0; i < 2^N; i += 2 DO:  
    T[i+1] = T[i] * T[i+1]  
    T[i] = T[i] + T[i+1]  
FOR m = 4; m <= 2^N; m *= 2 DO  
    FOR i = 0; i < 2^N; i += m:  
        T[i+m-1] = T[i+m-1] * T[i+m/2-1]  
        T[i] += T[i+m/2] * T[i+m/2-1]  
RETURN T[0]
```

Note that the loops in lines 1 and 5 can be executed in parallel. The following figure shows the case when $T$ has 8 items.

<p align="center">
  <img src="https://d2lkyury6zu01n.cloudfront.net/images/pic1.svg" width="800"/>
  <br>
  <em>Figure 1: Parallel evaluation of the ExpMinus1 algorithm for 8 items</em>
</p>


Finally, we add 1 to $T[0]$ to obtain the approximate (encrypted) values $E = [e^{z_0}, e^{z_1}, ..., e^{z_{n-1}}]$.

The error term in our approximation of $e^x$ is
$$
\begin{array}{rcl}
&&\frac{x^{K+1}}{(K+1)!} + \frac{x^{K+2}}{(K+2)!} + \ldots\cr
&<& \frac{x^{K+1}}{(K+1)!}(1 + \frac{x}{(K+2)} + \frac{x^2}{(K+2)^2} + \frac{x^3}{(K+2)^3} + \ldots).
\end{array}
$$
Obviously, the error term tends to 0 as $K$ tends to $\infty$. For a fixed $K$, the smaller $|x|$ yields a smaller error. Thus, to improve the precision, we can use

- a larger $K$
- a smaller $|x|$.

A larger $K$ will require more computation, so we prefer to reduce $|x|$. Using the identity below, we can scale $x$ to $x/q$. The cost is only $\log_2(q)$ squaring operations.
$$
e^x = (e^{x/q})^q
$$
We divide $z_i$ by, for example, $q = 8$ or $16$, compute the approximate values $E' = [e^{z_0/q}, e^{z_1/q}, \ldots, e^{z_{n-1}/q}]$, and then repeatedly square $E'$ three or four times to obtain the full $E = [e^{z_0}, e^{z_1}, \ldots, e^{z_{n-1}}]$.

### 2. Compute the sum

- Input: $E = [e_0, e_1, ..., e_{2^N-1}]$.  
- Output: $S = [s_0, s_1, ..., s_{2^N-1}]$ where $s_0 = s_1 = \ldots = s_{2^N-1} = \sum_{i=0}^{2^N-1} e_i$.

To sum all items in $E$, we repeatedly perform the "rotate-and-add" operation, as described in Algorithm 2.

**Algorithm 2**: Sum  
**In:** $E = [e_0, e_1, \ldots, e_{2^N-1}]$.  
**Out:** $S = [\sum_{i=0}^{2^N-1} e_i, \ldots, \sum_{i=0}^{2^N-1} e_i]$.
```
S = E  
FOR i = 1; i < 2^N; i *= 2 D 
  S += Rotate(S, i)  
RETURN S
```

An example is shown below.

<p align="center">
  <img src="https://d2lkyury6zu01n.cloudfront.net/images/pic2.svg" width="800"/>
  <br>
  <em>Figure 2: Stepwise execution of the sum algorithm for 8 items</em>
</p>


### 3. Invert the sum and multiply

- Input: $Z = [z_0, z_1, ..., z_{n-1}]$, $S = [s, s, ..., s]$ where $s =\sum_{i=0}^{2^N-1} z_i$.  
- Output: $\text{Softmax}(Z) = Z\cdot S^{-1} = [z_0/s, z_1/s, ..., z_{n-1}/s]$.

We simply use the OpenFHE library's native EvalDivide method; we only need to estimate the range of $s$. We shift the input vector $Z$ by subtracting its maximum element:
$$
\text{Softmax}(z_i) = \frac{e^{z_i - \max(Z)}}{\sum_{j=1}^{n} e^{z_j-\max(Z)}},
$$
then $s$ will be less than $n$.