# Encrypted Matrix Multiplication

*The article details the solution provided by the winner of the [Matrix Multiplication challenge](https://fherma.io/challenges/652bf669485c878710fd020b/overview).*

**Author:** [Aikata](https://www.iaik.tugraz.at/person/aikata-aikata/), Ph.D. student at TU Graz

Matrix multiplication is a crucial aspect of advanced mathematics and plays a central role in machine learning, especially in Neural Networks. Certain network components, like fully connected layers or filter/kernel, rely on matrix multiplication. Though there are efficient algorithms like Strassen's algorithm for plaintext operations, conducting matrix multiplication in an encrypted domain is a newer research area. This has gained attention because it enables encrypted ML training or inference using fully homomorphic encryption schemes like CKKS, which can handle approximate arithmetic.

Encrypted matrix multiplication techniques in literature can be broadly categorized into three types. The first type involves a depth of two multiplications and utilizes a simple row-wise encoding. An example is [this work](https://eprint.iacr.org/2023/1649.pdf), which presents a general technique. For a square matrix with dimensions $d\times d$, this method requires $2 d+3\log_2(d)-2$ rotations and $2d$ multiplications. It is important to note that these two operations are the most costly, as an expensive key-switch operation is needed after each one to ensure the ciphertext remains decryptable using the same secret key. A drawback of this approach is the necessity for $d^3$ slots packing availability in the ciphertext. Hence, it does not scale well for big matrices.

The second category of techniques, as described in [this paper](https://eprint.iacr.org/2018/1041.pdf), deviates slightly from previous methods by using diagonal-based matrix multiplication. Although this technique requires $3d+5\sqrt{d}$ rotations and $d$ ciphertext-ciphertext (ct-ct) multiplications initially, with increased packing ($d^3$ slots), it can be optimized to only need $d+2\sqrt{d}$ computations. However, a significant drawback is the requirement for three multiplicative depths. While the algorithms proposed in that paper can be modified to operate within a multiplicative depth of two, doing so results in a much more significant increase in the number of rotations and multiplications.

The third and final category of works, as presented in [1](https://eprint.iacr.org/2021/783.pdf), [2](https://eprint.iacr.org/2018/663.pdf) and [3](https://eprint.iacr.org/2018/1041.pdf), significantly diverges from the previous ones. These works aim to leverage a [multivariate variant of the CKKS scheme](https://eprint.iacr.org/2018/1245.pdf) (m-RLWE), enabling the encoding of a matrix into a hypercube structure. This approach facilitates cost-effective row-wise and column-wise rotations, optimizing matrix multiplication while only requiring a multiplicative depth of 2. However, note that the multivariate CKKS is incompatible with the original CKKS. Additionally, the parameters of the multivariate CKKS need to be standardized, and its [initial proposal](https://gpsc.uvigo.es/sites/default/files/publications/PedrouzoICASSP2015.pdf) was found to be insecure in [this paper](https://eprint.iacr.org/2018/966.pdf).

**Algorithm 1** Matrix.Mult (1 Matrix packing version of [this work](https://eprint.iacr.org/2023/1649.pdf))\
**Require:** $A,B \leftarrow$ row_enc $(\mathtt{A_{d\times d}},\mathtt{B_{d\times d}})$\
**Out:** $C=$ row_enc $(\mathtt{A_{d\times d}}\times\mathtt{B_{d\times d}})$

`// Preprocess A`\
1: &nbsp;**for** $j=0$ to $d-1$ **do**\
2: &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;$\tilde{A}[j] \leftarrow  \texttt{cMult}(A, \pi_{j} )$ `// Splitting A column-wise`\
3: &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;$\tilde{A}[j] \leftarrow  \texttt{Rot}(\tilde{A}[j],-j)$ `// Right align all the columns`\
4: &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;**for** $i=0$ to $\log_2(d)-1$}	**do** `// Replicate the columns`\
5: &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;$\tilde{A}[j] +=  \texttt{Rot}(\tilde{A}[j], -(2^i) )$

`// Preprocess B`\
6: &nbsp;**for** $j=0$ to $d-1$ **do**\
7: &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;$\tilde{B}[j] \leftarrow  \texttt{cMult}(B, \psi_{j} )$ `// Splitting B row-wise`\
8: &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;$\tilde{B}[j] \leftarrow  \texttt{Rot}(\tilde{B}[j],-j*d)$ `// Top align all the rows`\
9: &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;**for** $i=0$ to $\log_2(d)-1$ **do** `// Replicate the rows`\
10: &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;$\tilde{B}[j] += \texttt{Rot}(\tilde{B}[j], -(2^i)*d )$
 
`// Compute C`\
11: **for** $j=0$ to $d-1$ **do**\
12: &nbsp;&nbsp;&nbsp;&nbsp;$C += \texttt{cMult}(\tilde{A}[j],\tilde{B}[j] )$

Due to the FHERMA challenge restrictions, which limit the multiplicative depth to 2 and ciphertext encoding to row-wise, the latter two techniques are not applicable. Furthermore, naively applying the first one is not feasible when the available slots ($n=8192$) do not meet the requirement of $d^3$ slots for a given dimension of $d=64$. Therefore, we first explore adapting the technique from [this work](https://eprint.iacr.org/2023/1649.pdf) to our case. The adapted technique is outlined in the **Algorithm 1**, which utilizes column and row masks $\pi_i$ and $\psi_i$, respectively. The complexity of this adaptation is $2d+2d\log_2{d}-2$ rotations and $d$ ct-ct multiplications. Since it is possible to pack two matrices into one ciphertext, the algorithm can also be optimized to consume $2d+d\log_2{d}-1$ rotations by aligning rotations at Steps 3 and 8 and then packing two ciphertexts.

To optimize this further, we explore a strategy involving the initial packing of duplicate copies of the original ciphertext, one original and one rotated, which results in an even greater reduction in the number of rotations. The proposed **Algorithm 2** presents this approach, where both ciphertexts $A$ and $B$ undergo pre-processing. Following this packing strategy, only $d+d\log_2{d}+1$ rotations and $\frac{d}{2}$ multiplications are required for the subsequent steps.

**Algorithm 2** Optimized.Matrix.Mult\
**Require:** $A,B \leftarrow$ row_enc $(\mathtt{A_{d\times d}},\mathtt{B_{d\times d}})$\
**Out:** $C=$ row_enc $(\mathtt{A_{d\times d}}\times\mathtt{B_{d\times d}})$


`// Preprocess A`\
1: $A += \texttt{Rot}(A, -d*d+1)$\
2: **for** $j=0$ to $(d/2)-1$ **do**\
3: &nbsp;&nbsp;&nbsp;&nbsp;$\tilde{A}[j] \leftarrow \texttt{cMult}(A, \pi_{j,j+d*d})$ `// Splitting A column-wise`\
4: &nbsp;&nbsp;&nbsp;&nbsp;$\tilde{A}[j] \leftarrow \texttt{Rot}(\tilde{A}[j],-2j)$ `// Right align all the columns`\
5: &nbsp;&nbsp;&nbsp;&nbsp;**for** $i=0$ to $\log_2(d)-1$ **do** `// Replicate the columns`\
6: &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;$\tilde{A}[j] +=  \texttt{Rot}(\tilde{A}[j], -(2^i) )$

`// Preprocess B`\
7: &nbsp;$B +=  \texttt{Rot}(B, -d*d+d )$\
8: &nbsp;**for** $j=0$ to $(d/2)-1$ **do**\
9: &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;$\tilde{B}[j] \leftarrow  \texttt{cMult}(B, \psi_{j,j\+d\*d} )$ `// Splitting B row-wise`\
10: &nbsp;&nbsp;&nbsp;&nbsp;$\tilde{B}[j] \leftarrow  \texttt{Rot}(\tilde{B}[j],-2j*d)$ `// Top align all the rows`\
11: &nbsp;&nbsp;&nbsp;&nbsp;**for** $i=0$ to $\log_2(d)-1$ **do** `// Replicate the rows`\
12: &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;$\tilde{B}[j] +=  \texttt{Rot}(\tilde{B}[j], -(2^i)*d )$

`// Compute C`\
13: **for** $j=0$ to $(d/2)-1$ **do**\
14: &nbsp;&nbsp;&nbsp;&nbsp;$C += \texttt{cMult}(\tilde{A}[j],\tilde{B}[j] )$\
15: $C += \texttt{Rot}(c,d* d )$

Additionally, this algorithm exhibits high parallelizability. Hence, employing `pragma omp parallel` before the for loops can help leverage the capabilities of modern multithreaded operating systems, leading to excellent performance. It is important to highlight that the proposed approach is tailored to the constraints of the FHERMA challenge, considering the available packing $2d^2$ and matrix dimension $d$. Notably, the scalability of this approach improves with higher packing availability. It outperforms existing methods like [1](https://eprint.iacr.org/2023/1649.pdf) and [2](https://eprint.iacr.org/2018/1041.pdf) for $d^3$ slot-packing by consuming only $\mathcal{O}(\log_2{d})$ rotations while still requiring a multiplicative depth of 2. The proposed algorithm is quite simple, yet it achieves non-trivial results, particularly when applied to higher packing scenarios. Its effectiveness lies in improving the best-case outcomes.

Extending and applying the proposed approach to rectangular matrices and scenarios involving smaller matrix filters applied to a matrix present intriguing possibilities for future exploration. Generalizing the algorithm to handle different matrix shapes and sizes could enhance its versatility and applicability in various contexts within the field of privacy-preserving matrix multiplication.
