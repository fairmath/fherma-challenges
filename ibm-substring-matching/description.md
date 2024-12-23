# Introduction

This challenge was developed by  [IBM Research](https://research.ibm.com/).

The objective of the challenge substring matching, i.e., to find a small string or pattern in a large text, under CKKS.



This challenge is motivated by searching for a substring in a large public database where the querier wants to keep their search hidden. For example, This can be a public database of patents and the querier is a company that wants to check whether an invention they work on appears in the database without leaking details about their invention.

In what follows we use the following notation: $T$ is the large public text we search in, $n$ is its size, $s$ is the string we search for and $k$ is its size.

In cleartext there are many ways to search for a substring in a text:

1. The trivial way is to check (by comparing each letter of $s$ with the respective letter of $T$) whether $s$ appears in $T$ at position $i=1,2,\ldots, n-k$, which leads to an overall runtime of $O(nk)$.
2. A more efficient algorithm named after its authors Knuth-Morris-Pratt (KMP) achieves the much better runtime of $O(n+k)$. This is optimal since every algorithm needs to at least read $T$ and $s$ (assuming no preprocessing).
3. If we allow probabilistic algorithms we can compute a hash value $H(s)$ and compare it to the hashes computed on a sliding window $H(T[i:i+k])$, for $i=1,2,\ldots, n-k$. If $H(T[i+1:i+k+1])$ can be computed from $H(T[i:i+k])$ in $O(1)$ (for example, a CRC) this leads to a running time of $O(n+k)$.
4. Another approach for substring matching is to use a non-deterministic finite automaton (NDFA). A NDFA can be thought of a state-machine with states and rules defining how the NDFA translates from one state to another based on the input it sees. Here there are $k$ states corresponding to the $k$ prefixes of $s$, and when in state $i$ and depending on the next letter $T[c]$ read from $T$ the automaton moves to the states that correspond to states that correspond to prefixes of $s$ that end at $T[c]$. NDFAs can in fact match more than just strings, they can match a subset of regular expression, for example the '*','+' operators.


These methods were already studied under FHE (see for example, [1,2]).


For this challenge you will need to develop `strstr(s, k, T, n)` - a function that gets encrypted strings `s`, their sizes `k`, another string `T` and its size `n` (`k`, `T`, and `n` are given in cleartext). 
Note that unlike the C version this function gets a *batch* of strings (possibly of different sizes) to look for in `T`.
The function should return for each string in the batch the first positions where it appears in `T` (or -1 if it doesn't).
(Please see below for the exact definition of `strstr`)


[1] Genise, N., Gentry, C., Halevi, S., Li, B., Micciancio, D. (2019). Homomorphic Encryption for Finite Automata. In: Galbraith, S., Moriai, S. (eds) Advances in Cryptology – ASIACRYPT 2019. ASIACRYPT 2019. Lecture Notes in Computer Science(), vol 11922. Springer, Cham. https://doi.org/10.1007/978-3-030-34621-8_17

[2] Charlotte Bonte and Ilia Iliashenko. 2020. Homomorphic String Search with Constant Multiplicative Depth. In Proceedings of the 2020 ACM SIGSAC Conference on Cloud Computing Security Workshop (CCSW'20). Association for Computing Machinery, New York, NY, USA, 105–117. https://doi.org/10.1145/3411495.3421361




## Challenge info

1.  **Challenge type**: This challenge is a White Box challenge. Participants are required to submit the project with their source code. You can learn more about this type of challenges in our  [Participation guide](https://fherma.io/how_it_works).
2.  **Encryption scheme**: CKKS.
3.  **Supported libraries**:  [OpenFHE](https://github.com/openfheorg/openfhe-development)
4.  **Input**: Encrypted vector  $A=[x_1, \ldots, x_n]$, where  $x_i∈[0,255]$ are real numbers.
5.  **Output**: The outcome should be an encrypted vector of the sorted values of $A$.

## Parameters of the key

1.  **Bootstrapping**: for bootstrapping support.
2.  **Number of slots**:  $2^{16}$
3.  **Multiplication depth**: 29.
4.  **Fractional part precision (ScaleModSize)**:  59 bits.
5.  **First Module Size**: 60 bits.

## Parameters of the input

You are asked to implement one of these 4 versions:
1. `strstr_row(vector<ctxt>, s_row, vector<int> k, vector<char> T)` - here `s_row` is a vector of ctxts packed such that the j-th slot in `s_row[i]` holds the j-th letter of the i-th string (or 0 if the i-th string is shorter than i).
2. `strstr_col(vector<ctxt>, s_col, vector<int> k, vector<char> T)` - here `s_col` is a vector of ctxts packed such that the j-th slot in `s_col[i]` holds the i-th letter of the j-th string (or 0 if the j-th string is shorter than i).
3. `strstr_hybrid(CTileTensor<ctxt>, s_hybrid, vector<int> k, vector<char> T)` - here `s_hybrid` is a IBM's TileTensor. See below for details on TileTensor.

In all cases:
1. `k` is a vector of ints where `k[i]` is the length of the i-th word.
2. The size of `T` is given by the size of the vector.


In this challenge you can assume:
1. **string size** - The size of any string to search (i.e., `k[i]`) is at most 1024.
2. **number of strings** - The number of strings will be between at most 1024.
2. **text size** - The size of the text (i.e., `T`) is at most 4096.
3. **alphabet size** - All the letters of `T` (and of the strings in `s`) are lower-cap english letters encoded as: a=1, b=2, \ldots .

The sizes of the vectors in the input is set accordingly.

For example, if the strings to search are "hello" and "foo" the packing is going to be as follows:

`s_row` is going to be packed as
|   | Slot 0 | Slot 1 | Slot 2 | Slot 3| Slot 4| Slot 5| Slot 6| Slot 7| Slot 8|
|----------|----------|----------|----------|----------|----------|----------|----------|----------|-----------|
| s_row[0]    |     8     |      5    |       12   |     12     |    15      |    0      |    0      |    0      |     0      |
| s_row[1]   |       6   |   15       |    15      |    0      |     0     |    0      |     0     |      0    |     0      |


`s_col` is going to be packed as
|   | Slot 0 | Slot 1 |
|----------|----------|----------|
| s_row[0]    |     8     |      6    |
| s_row[1]   |       5   |   15       |
| s_row[2]   |       12   |   15       |
| s_row[3]   |       12   |   0       |
| s_row[4]   |       15   |   0       |


- for the hybrid version we will generate some input TileTensors with various shapes. Additionally, we will generate more TileTensors with shapes by demand.


## TileTensors
TileTensor is a data structure that allows for FHE code to be written in a packing-oblivious manner. That means that the same code works with different packing decisions and the packing decisions are made separately from the code, possibly at runtime. This means that you can write your code once and at runtime (for example, depending on the number of strings and their sizes) decide whether the packing be row-wise, column-wise or something hybrid such as packing multiple strings in a single row to utilize SIMD in a better way.

The intuition behind using TileTensors is to express your code as operating on tensors. Then, the mapping to ciphertexts is done independently to the codo. thinking of a ciphertext as a block (or "tile"), we cover the tensor with ciphertexts. The shape we give a single tile determines the packing. For example, a tile that has a single row (i.e., maps the slots of a ciphertext to a single row) will impose a row-wise packing; a tile that has a single column (i.e., maps the slots of a ciphertext to a single column) imposes a column-wise packing; and a tile that has 2 rows (i.e. maps the first half of the slots to one row and the second half of the slots a second row) imposes a packing with 2 strings in each ciphertext.

TileTensors are implemented in HElayers [download here: https://ibm.github.io/helayers/].
HElayers is a library developed by IBM Research that simplifies the use of FHE, making coding privacy preserving algorithms and specifically privacy preserving machine learning algorithms easier.

You can read more about TileTensors in [this tutorial from 2022 https://research.ibm.com/haifa/dept/vst/tutorial_ccs2022.html] and [this tutorial from 2023 https://research.ibm.com/haifa/dept/vst/tutorial_ccs2023.html].

Specifically for this challenge, you may be interseted in interleaved dimensions.




## Requirements of the output

1. **Packing**: The output should be a ciphertext $o$ where the $i$-th slot of $o$ holds the first position where $s[i]$ (the $i$-th input string) appears in $T$.
2. **Accuracy**: These values will be rounded to the nearest integer so they can incur an error of up to $0.49$.



## Timeline

-   **December 24, 2024**  - Start Date.
-   **March 30, 2025**  - Submission deadline.
-   **April 10, 2025**  - Prize awarded.

## Test environment

### Hardware

**CPU**:  12 core  **RAM**:  54 GB

### Software

The following libraries/packages will be used for generating test case data and for testing solutions:

-   **OpenFHE:**  v1.1.4
-   **OpenFHE-Python:**  v0.8.6

## Submission

To address this challenge, participants can utilize one of the two libraries, OpenFHE or Lattigo.

The executable should be named  `sort`  .

### OpenFHE

If the solution is developed using the OpenFHE library, we expect it to have a CMake project. The CMakeLists.txt file should be placed in the project's root directory. Please adhere to the following format when submitting your solution:

1.  **File format:**
    -   Your submission should be packed into a ZIP archive.
2.  **Structure of the archive:**
    -   Inside the ZIP archive, ensure there is a directory titled  `app`.
    -   Within the  `app`  directory, include your main  `CMakeLists.txt`  file and other necessary source files.


IMAGE HERE

#### Config file

You can use a config file to set parameters for generating a context on the server for testing the solution. An example of such a config and detailed description of each parameter is given below.

```none
{
    "indexes_for_rotation_key": [
        1
    ],
    "mult_depth": 29,
    "ring_dimension": 131072,
    "scale_mod_size": 59,
    "first_mod_size": 60,
    "batch_size": 65536,
    "enable_bootstrapping": false,
    "levels_available_after_bootstrap": 10,
    "level_budget": [4,4]
}

```


##### Parameters

-   **indexes_for_rotation_key**: if an application requires the use of a rotation key, this option allows specifying indexes for the rotation key. If the rotation key is not used, it should be an empty array:  `indexes_for_rotation_key=[]`.
    
-   **mult_depth**: the user can set the ring dimension. However, if a minimum ring dimension is set for the challenge, then the user can only increase this value; decreasing it is not possible.
    
-   **scale_mod_size**: this parameter is used to configure  `ScaleModSize`, default value is  `51`.
    
-   **first_mod_size**: this parameter allows setting up  `FirstModSize`, default value is  `60`.
    
-   **batch_size**: if the bootstrapping is not used, this parameter allows to set the batch size. Default value is  `ring_dimension/2`.
    
-   **enable_bootstrapping**: if you need bootstrapping, set this option to  `true`.
    
-   **levels_available_after_bootstrap**: this parameter allows setting up levels available after the bootstrapping if it's used. Note that the actual number of levels available after bootstrapping before next bootstrapping will be  `levels_available_after_bootstrap - 1`, because an additional level is used for scaling the ciphertext before next bootstrapping (in 64-bit CKKS bootstrapping).
    
-   **level_budget**: the bootstrapping procedure needs to consume a few levels to run. This parameter is used to call  `EvalBootstrapSetup`. Default value is [4,4].


### OpenFHE

-   **--input**  [path]: specifies the path to the file containing the encrypted vector.
- **--n** [size]: specifies the size of the array. The array will be written in slots $0,\ldots,(n-1)$ of the ciphertext.
-   **--output**  [path]: specifies the path to the file where the result should be written.
-   **--cc**  [path]: indicates the path to the crypto context file serialized in  **BINARY**  form.
-   **--key_public**  [path]: specifies the path to the Public Key file.
-   **--key_mult**  [path]: specifies the path to the Evaluation (Multiplication) Key file.
-   **--key_rot**  [path]: specifies the path to the Rotation Key file.


## Example

The executable will be run as follows:

```
./app --cc cc.bin --key_public pub.bin --key_mult mult.bin --input in.bin --output out.bin
```


An example for the message encrypted in  `in.bin`:  `Input = [203.23, 102.83, 3.68, 77.46]` (this does not include the noise added by CKKS during encryption.

An example output for this input:  `Output = [203.23, 102.83, 77.46, 3.68]`

## Evaluation Criteria

Submissions will be evaluated using an array of size $n=2048$ and scored with these criteria:

1.  **Correctness and accuracy:**  The output of the program for valid input (i.e., numbers in the range  $[0,255]$)  **must**  be correct (in descending order) with an error of no more than $0.0001$ for each element.
2.  **Execution time:**  The running time of the application on the provided input data.

That is, the winner will be the fastest application whose output is correct and accurate.

## Scoring & Awards

The winner will be awarded  **$4000**.


## Challenge Committee

-   [Gurgen Arakelov](https://www.linkedin.com/in/gurgen-arakelov-943172b9/), Fair Math
-   [Yuriy Polyakov](https://www.linkedin.com/in/yuriy-polyakov-796b84a/), Duality
-   [Hayim Shaul](https://www.linkedin.com/in/hayim-shaul-b2658/), IBM Research

## Useful Links

-   [FHERMA participation guide](https://fherma.io/how_it_works)—more about FHERMA challenges.
-   [OpenFHE](https://github.com/openfheorg/openfhe-development)  repository, README, and installation guide.
-   [OpenFHE Python](https://github.com/openfheorg/openfhe-python)  repository, README, and installation guide.
-   A vast collection of resources collected by  [FHE.org](http://fhe.org/)  [https://fhe.org/resources](https://fhe.org/resources), including tutorials and walk-throughs, use-cases and demos.
-   [OpenFHE AAAI 2024 Tutorial](https://openfheorg.github.io/aaai-2024-lab-materials/)—Fully Homomorphic Encryption for Privacy-Preserving Machine Learning Using the OpenFHE Library.

## Help

If you have any questions, you can:

-   Contact us by email:  [support@fherma.io](mailto:support@fherma.io)
-   Join our  [Discord](https://discord.gg/NfhXwyr9M5)  server, and ask your questions in the  [#fherma channel](https://discord.com/channels/1163764915803279360/1167875954392187030).
-   Open an issue in the  [GitHub Repository](https://github.com/Fherma-challenges/parity).
-   Use  [OpenFHE Discourse](https://openfhe.discourse.group/)  for OpenFHE related issues.


> Written with [StackEdit](https://stackedit.io/).