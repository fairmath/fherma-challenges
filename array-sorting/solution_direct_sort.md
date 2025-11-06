# Direct Sort for Encrypted Arrays of Real Numbers

*The article details the solution provided by the winners of the [Array Sorting challenge](https://fherma.io/challenges/66582c7551eafe1a4e6c451b).*

**Authors:** [Eymen Ünay](https://www.linkedin.com/in/eymen-unay/) (University of Edinburgh) and [Seunghu Kim](https://www.linkedin.com/in/seunghu-kim-11a556314/) (Chung-Ang Universitiy, Republic of Korea)

# Overview of the approach
Sorting an encrypted array is challenging because we do not have access to comparison results. This makes efficient sorting algorithms like Merge Sort and Quick Sort hard to adopt in blind sorting because their work depends on comparison results. 
A common solution to blind sorting is using a sorting network, which was proposed by Batcher  due to its deterministic property. However, sorting networks such as Bitonic Sort and Odd-Even Merge Sort have multiple comparison stages, which result in deeper sorting circuits. Furthermore, the number of repeated rounds of comparisons increases as the array size $N$ grows

Thus, Çetin et al. proposed a depth-optimized sorting method called Direct Sort [2,3]. We have adopted Direct Sort to CKKS for the challenge, which we optimize for real number arrays and fully packed ciphertexts. Our sorting method consists of two phases: *rank construction* and *rotation index checking*.


## Rank construction

In this phase, we evaluate the rank ciphertext, where each slot denotes the number of entries smaller than itself. To count the rank, we sum up all comparison results as follows:

$$\text{Rank} = \sum_{i=1}^{N} \text{Comp}(\mathbf{A}, \text{Rot}(\mathbf{A}, i))$$

To compare real numbers, we employ a composite approximation of the sign function presented in [4]. Specifically, we used a degree-15 polynomial $f$ and a degree-27 polynomial $g$. Additionally, we set both $df$ and $dg$ to 3, meaning that $g$ is composed 3 times, followed by 3 evaluations of $f$. As a result, the total circuit depth for the sign evaluation, meeting the challenge requirement of a 0.01 difference within the range of real numbers [0, 255], was 27. Figure 1 describes an example of rank construction.
    
<p align="center">
  <img src="https://corrida-public.s3.us-west-2.amazonaws.com/static/rank_construction+(1).png" width="400"/>
  <br>
  <em>Figure 1: Example of rank construction</em>
</p>

## Rotation index checking

In this phase, we complete the sorting based on the rank. Our main idea is that Index-Rank denotes the rotation indices for each entry to be sorted, where $\textsf{Index}$ is a packed plaintext of indices.

<p align="center">
  <img src="https://corrida-public.s3.us-west-2.amazonaws.com/static/rotation_checking.png" width="400"/>
  <br>
  <em>Figure 2: Example of Index - Rank</em>
</p>


To handle symmetric rotations within the array bound, we define $\textsf{DoubledSinc}(x) = \textsf{Sinc}(x) + \textsf{Sinc}(x+N)$ function, where $N$ is a length of array and $\textsf{Sinc}$ is defined as follows:

$$\text{Sinc}(x) =
\begin{cases}
1, & \text{if } x = 0, \\
\dfrac{\sin(x)}{x}, & \text{otherwise.}
\end{cases}$$

Then, we can use $\textsf{DoubledSinc}(\textsf{Index} - \textsf{Rank} - i)$ as a masking vector for $\mathbf{A}$ to leave only the entries to be rotated by $i$. Finally, for $i = 1, \dots, N-1$, rotation index checking can be described as follows:

$$\text{Sorted} = \sum_{i=0}^{N-1} \text{Rot}(\mathbf{A}, i) \odot \text{DoubledSinc}(\text{Index} - \text{Rank} - i)$$


# Optimizations
Our approach is efficient in the sense of requiring a single comparison stage regardless of array size N, which keeps the entire circuit shallow. However, it requires O(N) comparisons and $\textsf{DoubledSinc}$ evaluations, which are computationally intensive. Thus, we transform the loop into a SIMD operation by batching the polynomial evaluations.

## Optimized rank construction

We make the input array $\mathbf{A}$ N-fold. Since it has the same internal structure as the sparse packed $\mathbf{A}$, we can treat it as an $N^2$ array without additional cost. Additionally, we pack $N-1$ rotations of $\mathbf{A}$ into a single ciphertext. We denote the N-fold $\mathbf{A}$ as $\textsf{Dup}(\mathbf{A})$ and the packed rotations as $\textsf{Rots}(\mathbf{A})$ as follows:

$$
\textsf{Dup}(\mathbf{A}) = [A \;|\; A \;|\; \dots \;|\; A]
$$

$$
\textsf{Rots}(\mathbf{A}) = [\,\textsf{Rot}(A,1) \;|\; \textsf{Rot}(A,2) \;|\; \dots \;|\; \textsf{Rot}(A,N-1) \;|\; \varnothing\,]
$$

In this way, we need to perform only one comparison, $\textsf{Comp}(\textsf{Dup}(\mathbf{A}), \textsf{Rots}(\mathbf{A}))$. After that, we column-sum the comparison result to get rank ciphertext.

## Rank Folding Optimization

We have optimized the rank construction further by using the knowledge of $\textsf{Comp}(a,b) = 1 - \textsf{Comp}(b,a)$ since the underlying Sign is an odd function. In terms of batching we have the $\textsf{Comp}(\mathbf{A},\textsf{Rot}(\mathbf{A},k)) = 1 - \textsf{Rot}(\textsf{Comp}(\mathbf{A},\textsf{Rot}(\mathbf{A}, N - k)), k)$ relation.  We can "fold" the rank by only calculating the half of comparisons for rotations smaller than N/2 and then inferring the rest of the comparison by using the information available. We have placed the rotations $i$ up to N/2 in batch pairs and we have used the pair $i$ to obtain the comparison result of $N - i$. Since a column-sum will be done the placement of the rotated values is not affecting the result.

$$
\textsf{Dup}(\mathbf{A}) = [A \;|\; A \;|\; \dots \;|\; A]
$$

$$
\textsf{Rots}(\mathbf{A}) = [ \textsf{Rot}(A,1) \;|\; \textsf{Rot}(A,1) \;|\; \textsf{Rot}(A,2) \;|\; \textsf{Rot}(A,2) \;|\; \dots ]
$$

$$
\textsf{Comp}(\textsf{Dup}, \textsf{Rots}) = [ \textsf{Comp}(A,A_1) \;|\; \textsf{Comp}(A,A_1) \;|\; \textsf{Comp}(A,A_2) \;|\; \textsf{Comp}(A,A_2) \;|\; \dots ]
$$

$$
\textsf{HalfComp}(\textsf{Dup}, \textsf{Rots}) = [ \textsf{Comp}(A,A_1) \;|\; 0 \;|\; \textsf{Comp}(A,A_2) \;|\; 0 \;|\; \dots ]
$$


After post-processing the comparison result, we will get a rank identical to before the optimization, only with the rotations smaller than N/2 being in odd batch indices and rotations larger than N/2 being in the even batches. The difference is we did not do the rotations larger than N/2 and skipped half of rotations.

The comparison result should be divided into half by zeroing even batches, the second batch of batch pairs, to get the direct result of the rotations smaller than N/2.

For rotations larger than N/2 (i.e., N - i), we can derive the comparison result by inverting the result of rotation $i$.
This process works by rotating the full comparison result by $i$ and then inverting the bits by subtracting from 1. 


This optimization moved N/2 rotations from the higher levels which are very expensive to the lower level after the comparison which run faster.

## Optimized rotation index checking

Rotation index checking can be optimized in a similar manner. First, we make a 2N-fold $\textsf{Index} - \textsf{Rank}$ ciphertext. Additionally, we use a stretched checking vector which has N entries for all possible rotation indices, thus having a length of $2N^2$. The following is an example:
$$
[0, \dots, 0, 1, \dots, 1, \dots, N, \dots, N, -1, \dots, -1, \dots, -N+1, \dots, -N+1]
$$

Then, we can evaluate $\textsf{Sinc}$ function once as:
$$
\textsf{Sinc}(\textsf{Dup}(\textsf{Index} - \textsf{Rank}) - \textsf{stretched})
$$


By combining a depth efficient algorithm with SIMD batching we have developed a shallow and fast sorting solution. Due to its low depth, it can be used in more FHE applications conveniently. The lack of bootstrapping can enable more use of the sorting algorithm in various FHE contexts. 

# References

1. Kenneth E. Batcher. Sorting networks and their applications. In American Federation of Information Processing Societies: AFIPS Conference Proceedings: 1968 Spring Joint Computer Conference, volume 32 of AFIPS Conference Proceedings, pages 307–314. Thomson Book Company, Washington D.C., 1968.

2. Gizem S. Çetin, Yarkın Doröz, Berk Sunar, and Erkay Savaş. Depth optimized efficient homomorphic sorting. In Progress in Cryptology - LATINCRYPT 2015, volume 9230 of Lecture Notes in Computer Science, pages 61–80. Springer, 2015.

3. Gizem S. Çetin and Berk Sunar. Homomorphic rank sort using surrogate polynomials. In Progress in Cryptology - LATINCRYPT 2017, volume 11368 of Lecture Notes in Computer Science, pages 311–326. Springer, 2017.

4. Jung Hee Cheon, Dongwoo Kim, and Duhyeong Kim. Efficient homomorphic comparison methods with optimal complexity. In Advances in Cryptology - ASIACRYPT 2020, Part II, volume 12492 of Lecture Notes in Computer Science, pages 221–256. Springer, 2020.
