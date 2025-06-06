# Encrypted Array Sorting

*The article details the solution provided by the winner of the [Array Sorting challenge](https://fherma.io/challenges/66582c7551eafe1a4e6c451b).*

**Author:** [Chi-Hieu Nguyen](https://www.linkedin.com/in/hieu-nguyen-ba6548316), University of Technology Sydney, Australia.

## Introduction

The objective of the challenge is to sort an encrypted array of real values. Sorting under approximate HE, such as the CKKS scheme, presents unique challenges due to the inherent noise introduced by the scheme. This noise grows with each operation, further amplified by the inaccuracies in the polynomial approximations used for comparisons.

## Approach

The proposed solution comprises two main steps:

### Step 1: Index Calculation
For each value in the array, we determine its target index by counting the number of values smaller than it. This involves pairwise comparisons of all array elements. To facilitate these comparisons, the current value is subtracted from every other value, and the result is passed through an approximated sign function. These pairwise comparisons are performed simultaneously in a SIMD fashion within a single packed ciphertext containing $2^{15} = 32,768$ slots. This process requires several rotations to duplicate values across the ciphertext slots. **Figure 1** illustrates the computation of target indices.

![fherma-sorting](https://d2lkyury6zu01n.cloudfront.net/images/hita-sort-1.png)

***Figure 1**: A toy example illustrating the computation of sorted indices for an input array of size 4.*


To perform the comparison, we approximate the sign function using a composite polynomial approach as described in [1]. Specifically, three polynomials of ![image](https://hackmd.io/_uploads/HkPtPO4XJx.png)
degree 63 are employed to approximate the function within the range $[-255, -0.01] \cup [0.01, 255]$ to satisfy the challenge requirements. **Figure 2** depicts the approximation, with a maximum absolute error below $0.0001$. Polynomial evaluations are done using the baby-step giant-step (BSGS) algorithm [2] to optimize level consumption. The comparison circuit utilizes 19 levels in total ($1 + 3\lceil\log_2{63}\rceil$), including an additional level for input value scaling. After applying the comparison function, rotation and summation operations are performed to accumulate results and compute the target indices (**Figure 1**).

![fherma_sorting_4](https://d2lkyury6zu01n.cloudfront.net/images/hita-sort-2.png)


***Figure 2**: Approximation of the sign function using a composition of three polynomials $p_1, p_2, p_3$ of degree 63.*
 
### Step 2: Permutation
A permutation matrix is derived based on the computed indices, as demonstrated in **Figure 3**. This process requires an approximated equality-checking function, which is constructed as a composition of two polynomials with degrees 59 and 62, as shown in **Figure 4**. The array is then rearranged into sorted order using vector-matrix multiplication with the permutation matrix. This step consumes a total of 14 levels, obtained by $\lceil\log_2{59}\rceil + \lceil\log_2{62}\rceil + 2$, where the additional two levels account for multiplication with the permutation matrix and a masking operation.

![fherma-sorting-Page-2](https://d2lkyury6zu01n.cloudfront.net/images/hita-sort-3.png)

***Figure 3**: Computation of the permutation matrix from the indices, followed by the rearrangement of array elements into sorted order.*


![fherma_sorting_5'](https://d2lkyury6zu01n.cloudfront.net/images/hita-sort-4.png)

***Figure 4**: Approximation of the equality checking function using a composition of three polynomials $p_4,p_5$ of degree 59 and 62.*


## References

[1] **Lee, Eunsang**, et al. "Minimax approximation of sign function by composite polynomial for homomorphic comparison." *IEEE Transactions on Dependable and Secure Computing* 19.6 (2021): 3711-3727.

[2] **J.-P. Bossuat, C. Mouchet, J. Troncoso-Pastoriza and A.-P. Hubaux**, "Efficient bootstrapping for approximate homomorphic encryption with non-sparse keys", *Proc. EUROCRYPT*, pp. 587-617, 2021.