# k-Nearest Neighbors Search under FHE

*The article details the solution provided by the winner of the [k-Nearest Neighbors Search challenge](https://fherma.io/challenges/6789154e1597b29897d448a4/overview).*

**Author:** [Chi-Hieu Nguyen](https://www.linkedin.com/in/hieu-nguyen-ba6548316), University of Technology Sydney, Australia.

## Introduction

The challenge tasks players with finding the $k$ nearest neighbors of an encrypted 2D vector within a database, using cosine similarity to measure the distance between vectors. Cosine similarity is defined as $d(\mathbf{u}, \mathbf{v}) = 1 - \frac{\mathbf{u} \cdot \mathbf{v}}{|\mathbf{u}| |\mathbf{v}|}$, where $\mathbf{u}$ and $\mathbf{v}$ are vectors, $\cdot$ denotes the dot product, and $|\cdot|$ represents the Euclidean norm. A common approach to find $k$-nearest neighbors (kNN) in cleartext is to compute the cosine similarity between the query vector and all database vectors, sort the similarities in descending order, and select the top $k$ vectors. This can be optimized using data structures like KD-trees or approximate methods like locality-sensitive hashing for efficiency.

However, a naive implementation of such an algorithm in the HE domain may incur significant overhead due to the high computational cost of encrypted arithmetic operations, the need for deep circuits to evaluate non-linear functions like division and square roots in cosine similarity, limited support for comparison and sorting operations, and the increased ciphertext size and noise growth in HE schemes.


## Approach

We adopted an approximated approach that simplifies the kNN problem into a lookup table. This is based on the observation that two vectors are likely to share similar neighbors if the angle between them is small. In particular, we partition the 2D plane into $M$ uniform angular sectors, defined by a set of $M$ vectors $ \{v_0, v_1, \dots, v_{M-1}\} $, where each $v_i$ is equally spaced at angles $\frac{2\pi i}{M}$ from the origin. Here, the $i$-th sector is the sector between $v_{i-1}$ and $v_i$. The neighbor set of a sector is defined as the $k$ nearest neighbors of its bisector ray, precomputed during initialization. For a query vector $x$, we identify the sector it falls into by computing its angle relative to the origin and return the precomputed neighbors of that sector as its approximate neighbors. Figure 1 illustrates this partitioning approach.

![sector_partition](https://d2lkyury6zu01n.cloudfront.net/images/hita-knn-1.png)

***Figure 1**: Illustration of the angular sector partitioning approach with $M=50$ sectors.*

Given a 2D query vector $x$, we can determine if it falls into the $i$-th sector by evaluating the dot products $x \cdot v_{i-1}$ and $x \cdot v_i$ and checking if these values have opposite signs. In the HE domain, this check can be translated to computing the product of the dot products, i.e., $(x \cdot v_{i-1}) \cdot (x \cdot v_i) = (x[0]v_{i-1}[0] + x[1]v_{i-1}[1]) * (x[0]v_i[0] + x[1]v_i[1])$, using basic HE operations. We then apply an approximation of the sign function to the result to check if the value is negative, confirming sector membership.

It's straightforward that the accuracy of the prediction increases as the number of sectors increases, though this comes at the cost of higher computational requirements. At a very large number of clusters, the accuracy approaches perfection, but the computational cost may become excessively high. However, given the nonuniform distribution of data points, we can employ a nonuniform clustering approach to reduce the number of clusters. This involves denser partitioning in directions with more points and coarser partitioning in less populated areas. Specifically, we start with a high-resolution partition of $M=5000000$ clusters, which achieves perfect accuracy, and then gradually reduce the number of clusters by merging consecutive clusters that share the same set of $k$ nearest neighbors. This process is repeated until no further merging is possible, resulting in $M=1001$ clusters after the procedure, significantly reducing the computational overhead. Figure 2 shows an illustration of the resulting nonuniform partition. The high-level pseudocode for reducing the number of clusters is as follows

```
> For each sector:
>     Compute k nearest neighbors of the sector's center
>     Store the neighbor set in a map
> 
> Sort sectors in ascending order of start angle
> 
> Initialize an empty list for merged sectors
> While there are sectors to process:
>     Group consecutive sectors with the same k-NN set
>     Merge each group into a single sector
>     Add the merged sector to the list
> Update the sector list with the merged sectors
```

![nonuniform](https://d2lkyury6zu01n.cloudfront.net/images/hita-knn-2.png)

***Figure 2**: Illustration of the resulting nonuniform partition after merging clusters.*

## HE Implementation

We now describe the HE implementation for determining the sector of a query vector $\mathbf{x}$ and mapping it to the corresponding precomputed $k$ nearest neighbors, using the sector-based approximation approach. The process is broken down into multiple steps as follows.

* **Step 0:** The process starts with a ciphertext $\text{ct}_\mathbf{x}$ containing the 2D query vector $\mathbf{x} = [x[0], x[1]]$. The components $x[0]$ and $x[1]$ are placed in the first two slots of the ciphertext, with all subsequent slots set to zero.
* **Step 1: Replicate the query vector across slots**\
    To enable simultaneous computation across multiple sectors, the query vector $\mathbf{x}$ is replicated across the ciphertext slots. After replication, each pair of slots in $\text{ct}_\mathbf{x}$ (e.g., slots 0–1, 2–3, etc.) contains the values $[x[0], x[1]]$.
* **Step 2: Make a plaintext for sector boundary vectors**\
    A plaintext $\text{pt}_\mathbf{v}$ is created to store the sector boundary vectors ${\mathbf{v}_0, \mathbf{v}_1, \dots, \mathbf{v}_M}$. For each sector $i$, the vector $\mathbf{v}_i$ is placed in specific slot pairs. For example, slots from $32i$ to $32i+31$ corresponding to sector $i$ will contain the replications of $[\mathbf{v}_i[0], \mathbf{v}_i[1]]$. This allows for the computation of dot products with consecutive sector boundaries.
* **Step 3: Compute dot products with sector boundaries**\
    For each sector $i$, the dot products $x \cdot v_{i-1}$ and $x \cdot v_i$ are computed in the HE domain. This involves element-wise subtraction between the replicated query vector and the sector boundary vectors, followed by rotation and multiplication. Specifically, the dot product $x \cdot v_i$ is calculated as $(\text{ct}_x-\text{pt}_v)*\text{Rotate}(\text{ct}_x-\text{pt}_v, 1)$.
* **Step 4: Determine the sign of dot products**\
    To check if $x$ lies between $v_{i-1}$ and $v_i$, we need to determine if the dot products $x \cdot v_{i-1}$ and $x \cdot v_i$ have opposite signs. An approximation of the sign function is evalutated over the dot product results using Paterson-Stockmeyer algorithm, converting the numerical dot products into boolean indicators (1 if the dot product is positive and 0 if negative).
* **Step 5: Identify sector**\
    The sector membership test relies on the fact that $x$ lies in sector $i$ if $(x \cdot v_{i-1}) \cdot (x \cdot v_i) < 0$, indicating opposite signs. In the HE domain, this is implemented by multiplying the sign indicators of the two dot products. If the product is 1 (i.e., one sign is positive and the other negative), $x$ is confirmed to be in sector $i$.
* **Step 6: Map to precomputed neighbors**\
    Once the sector of $x$ is identified, the precomputed $k$ nearest neighbors associated with that sector are retrieved. These neighbors were calculated during the preprocessing phase for each sector's bisector ray. The neighbor sets are encoded into a single plaintext and is assigned to the slots corresponding to the identified sector by multiplication, ensuring that the output ciphertext only contains the approximate $k$ nearest neighbors of $x$.
* **Step 7: Accumulate neighbors to the first 10 slots using rotation**
