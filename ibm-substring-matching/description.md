# Introduction

This challenge was developed by [IBM Research](https://research.ibm.com/).

The objective of the challenge is substring matching, i.e., to find small strings in a large text, under CKKS.

This challenge is motivated by searching for a substring in a large public database where the querier wants to keep their search hidden. For example, This can be a public database of patents and the querier is a company that wants to check whether an invention they work on already appears in the database without leaking details about their invention.

In what follows we use the following notation: $T$ is the large public text we search in, $n$ is its size, $s$ is the string we search for and $k$ is its size.

In cleartext there are several ways to search for a substring in a text:

1. The trivial way is to check (by comparing each letter of $s$ with the respective letter of $T$) whether $s$ appears in $T$ at position $i=1,2,\ldots, n-k$, which leads to an overall runtime of $O(nk)$.
2. A more efficient algorithm named after its authors Knuth-Morris-Pratt (KMP) achieves the much better runtime of $O(n+k)$. This is optimal since every algorithm needs to at least read $T$ and $s$ (assuming no preprocessing).
3. If we allow probabilistic algorithms we can compute a hash value $H(s)$ and compare it to the hashes computed on a sliding window $H(T[i:i+k])$, for $i=1,2,\ldots, n-k$. If $H(T[i+1:i+k+1])$ can be computed from $H(T[i:i+k])$ in $O(1)$ (for example, a CRC) this leads to a running time of $O(n+k)$.
4. Another approach for substring matching is to use a non-deterministic finite automaton (NDFA). A NDFA can be thought of a state-machine with states and rules defining how the NDFA translates from one state to another based on the input it sees. Here there are $k$ states corresponding to the $k$ prefixes of $s$, and when in state $i$ and depending on the next letter $T[c]$ read from $T$ the automaton moves to the states that correspond to states that correspond to prefixes of $s$ that end at $T[c]$. NDFAs can in fact match more than just strings, they can match a subset of regular expression, for example the '*','+' operators. 

These NDFA methods have already been studied under FHE (see the Useful Links section for more details)

For this challenge, you need to implement `strstr(words, wordSize, T)`, a function that takes multiple encrypted strings (`words`), their corresponding sizes (`wordSize`), and a text (`T`), where `wordSize` and `T` are provided in cleartext. Unlike the C version, this function processes a batch of strings, which may vary in length. For each string in the batch, the function should return the position of its first occurrence in `T`, or `-1` if it is not found.



## Challenge info

1.  **Challenge type**: This challenge is a White Box challenge. Participants are required to submit the project with their source code. You can learn more about this type of challenges in our  [Participation guide](https://fherma.io/how_it_works).
2.  **Encryption scheme**: CKKS.
3.  **Supported libraries**: [HElayers](https://ibm.github.io/helayers/).

## Parameters of the key

1.  **Bootstrapping**: for bootstrapping support.
2.  **Number of slots**:  $2^{16}$
3.  **Multiplication depth**: 29.
4.  **Fractional part precision (ScaleModSize)**:  59 bits.
5.  **First Module Size**: 60 bits.

## Parameters of the input

At the heart of the challenge, you are asked to implement this function:
 `strstr(ENCRYPTED_TYPE_SEE_BELOW words, vector<int> wordSize, vector<char> T)`

where:
1. `T` is the text (in the clear) that is needed to be searched in. The size of the text is given by size of the vector.
2. `wordSize` is a vector of ints indicating the sizes of the words that are searched for in `T`. The value `wordSize[i]` is the length of the $i$-th word. The size of this vector indicates the number of words that need to be searched for.
3. `words` is the words that need to be searched for. You have the choice of getting it as a vector of ciphertexts or as a TileTensor structure (see below about TileTensors).

If you choose to get `ctxts` as a vector of ciphertexts then you can choose one of two packings: row-based and column-based.

For **row-based packing**, `words` is a vector of ciphertexts packed such that the $j$-th slot in `words[i]` holds the $j$-th letter of the $i$-th string (or 0 if the $i$-th string is shorter than $i$).

For example, if the strings to search are "Hello" and "foo" then `words` is going to be packed as:

|   | Slot 0 | Slot 1 | Slot 2 | Slot 3| Slot 4| Slot 5| Slot 6| Slot 7| Slot 8|
|----------|----------|----------|----------|----------|----------|----------|----------|----------|-----------|
| words[0]    |     72     |      101    |       108   |     108     |    111      |    0      |    0      |    0      |     0      |
| words[1]   |       102   |   111       |    111      |    0      |     0     |    0      |     0     |      0    |     0      |


For **column-based packing**, `words` is a vector of ctxts packed such that the $j$-th slot in `words[i]` holds the $i$-th letter of the $j$-th string (or 0 if the $j$-th string is shorter than $i$).

For example, if the strings to search are "Hello" and "foo" then `words` is going to be packed as:

|   | Slot 0 | Slot 1 |
|----------|----------|----------|
| words[0]    |     72     |      102    |
| words[1]   |       101   |   111       |
| words[2]   |       108   |   111       |
| words[3]   |       108   |   0       |
| words[4]   |       111   |   0       |


For **hybrid packing**, `words` is IBM's CTileTensor (see below for details on TileTensors). You can ask for the input to be encoded with different tile shapes. For example, if you ask for a tile shape of $[5/8, 2, 1/a]$ (where $8\cdot t = slotNum$) you get the input in column-based packing.
If you you ask for a tile shape of $[5, 2/2, 1/a]$ (where $2\cdot t = slotNum$) you get the input in row-based packing.
If you ask for a tile shape of $[5/8, 2/2, 1/a]$ (where $8\cdot 2\cdot t = slotNum$) you get the input in a hybrid shape:

|   | Slot 0 | Slot 1 | Slot 2 | Slot 3| Slot 4| Slot 5| Slot 6| Slot 7| Slot 8| slot 9| Slot 10 | Slot 11 | Slot 12 | Slot 13| Slot 14| Slot 15| Slot 16|
|------|----|---|-------|----|------|-------|---|-----|-----|------|----|----|------|-----|-----|----|----|
| $1^{st}$ ctxt    |     72|102     |      101|111    |       108|111   |     108|0     |    111|0      |    0|0      |    0|0      |    0|0      |     0|0      |


## TileTensors
TileTensor is a data structure that allows for FHE code to be written in a packing-oblivious manner. That means that the same code works with different packing decisions and the packing decisions are made separately from the code, possibly at runtime. This means that you can write your code once and at runtime (for example, depending on the number of strings and their sizes) decide whether the packing be row-wise, column-wise or something hybrid such as packing multiple strings in a single row to utilize SIMD in a better way.

The intuition behind using TileTensors is to express your code as operating on tensors. Then, the mapping to ciphertexts is done independently to the code. thinking of a ciphertext as a block (or "tile"), we cover the tensor with ciphertexts. The shape we give a single tile determines the packing. For example, a tile that has a single row (i.e., maps the slots of a ciphertext to a single row) will impose a row-wise packing; a tile that has a single column (i.e., maps the slots of a ciphertext to a single column) imposes a column-wise packing; and a tile that has 2 rows (i.e. maps the first half of the slots to one row and the second half of the slots a second row) imposes a packing with 2 strings in each ciphertext.

TileTensors are implemented in [HElayers](https://ibm.github.io/helayers/).
HElayers is a library developed by IBM Research that simplifies the use of FHE, making coding privacy preserving algorithms and specifically privacy preserving machine learning algorithms easier.

You can read more about TileTensors in [this tutorial from 2022](https://research.ibm.com/haifa/dept/vst/tutorial_ccs2022.html) and [this tutorial from 2023](https://research.ibm.com/haifa/dept/vst/tutorial_ccs2023.html).

Specifically for this challenge, you may be interested in interleaved dimensions.

## Requirements of the output

1. **Packing**: The output should be a ciphertext $o$ where the $i$-th slot of $o$ holds the first position where $s[i]$ (the $i$-th input string) appears in $T$.
2. **Accuracy**: These values will be rounded to the nearest integer so they can incur an error of up to $0.49$.

## Timeline

-   **Feb 04, 2025**  - Start Date.
-   **May 04, 2025**  - Submission deadline.
-   **May 15, 2025**  - Prize awarded.

## Test environment

### Hardware

- **CPU:** 12 cores
- **RAM:** 54 GB

### Software

The following libraries/packages will be used for generating test case data and for testing solutions:

-   **HElayers:** v1.5.4

## Submission

To address this challenge, participants can utilize the HElayers library.

The executable should be named `strstr`.

#### Config file

You can use a config file to set parameters for generating a context on the server for testing the solution. An example of such a config and detailed description of each parameter is given below.

```json
{
    "indexes_for_rotation_key": [
        1
    ],
    "mult_depth": 29,
    "ring_dimension": 131072,
    "scale_mod_size": 51,
    "first_mod_size": 60,
    "batch_size": 65536,
    "enable_bootstrapping": true,
    "levels_available_after_bootstrap": 10,
    "level_budget": [4,4]
}
```

**Parameters:**

- **indexes_for_rotation_key**: if an application requires the use of a rotation key, this option allows specifying indexes for the rotation key. If the rotation key is not used, it should be an empty array: `indexes_for_rotation_key=[]`.
- **mult_depth**: the user can set the ring dimension. However, if a minimum ring dimension is set for the challenge, then the user can only increase this value; decreasing it is not possible. 
- **scale_mod_size**: this parameter is used to configure `ScaleModSize`, default value is `51`. 
- **first_mod_size**: this parameter allows setting up `FirstModSize`, default value is `60`. 
- **batch_size**: if the bootstrapping is not used, this parameter allows to set the batch size. Default value is `ring_dimension/2`. 
- **enable_bootstrapping**: if you need bootstrapping, set this option to `true`.  
- **levels_available_after_bootstrap**: this parameter allows setting up levels available after the bootstrapping if it's used. Note that the actual number of levels available after bootstrapping before next bootstrapping will be `levels_available_after_bootstrap - 1`, because an additional level is used for scaling the ciphertext before next bootstrapping (in 64-bit CKKS bootstrapping).
- **level_budget**: the bootstrapping procedure needs to consume a few levels to run. This parameter is used to call `EvalBootstrapSetup`. Default value is [4,4]. 

## Command-line interface for application testing

The application must support the Command Line Interface (CLI) specified below.

### Helayers

-   **--input** [path]: specifies the path to the file containing the encrypted vector.
- **--word_size** [size]: specifies the size of the array. The array will be written in slots $0,\ldots,(n-1)$ of the ciphertext.
-   **--output** [path]: specifies the path to the file where the result should be written.
-   **--cc** [path]: indicates the path to the crypto context file serialized in  **BINARY**  form.
-   **--key_pub** [path]: specifies the path to the Public Key file.
-   **--key_mult** [path]: specifies the path to the Evaluation (Multiplication) Key file.
-   **--key_rot** [path]: specifies the path to the Rotation Key file.

## Examples
Below we give a few examples for the different packing options. You can plan for different packings for the different testcases you will be evaluated on but you must submit a single code.

The input is integer numbers in the range $[0,255]$. The clear text we search in is given encoded in ascii. For convenience, in the examples below include values whose ascii codes are visible ascii but you should expect non-visible ascii as well. For example, the input text may be given as:
`--text=Hello` which is equivalent to 
`--text=$'\x48\x65\x6c\x6c\x6f'` and it may also be given as the non visible text:
`--text=$'\x01\x02\x03\x04\x05'`

### Row-based packing
In this example we want to find the words "hello", "world" in the text "hello world"

The executable will be run as follows:
```
./app --cc cc.bin --key_public pub.bin --key_mult mult.bin --input in_row.bin --word_size 5,5 --output out.bin --text "hello world"
```

The file `in_row.bin` will include 2 ciphertexts (the noise added by CKKS during encryption is not shown): 
- `Ctxt1 = ['h', 'e', 'l', 'l', 'o', 0, ...]` 
- `Ctxt2 = ['w', 'o', 'r', 'l', 'd', 0, ...]`

The file `out_row.bin` will include 2 ciphertexts: 
- `Ctxt1 = [0, X, X, ...]`
- `Ctxt2 = [6, X, X, ...]`, where `X` indicates a don't-care value.

### Col-based packing
In this example we want to find the words "he", "ll", "wo", "rd", "no" in the text "hello world"

The executable will be run as follows:
```
./app --cc cc.bin --key_public pub.bin --key_mult mult.bin --input in_col.bin --word_size 2,2,2 --output out.bin --text "hello world"
```

The file `in_col.bin` will include 2 ciphertexts (the noise added by CKKS during encryption is not shown):
- `Ctxt1 = ['h', 'l', 'w', 'r', 'n', 0, ...]`
- `Ctxt2 = ['e', 'l', 'o', 'd', 'o', 0, ...]` 

The file `out_row.bin` will include 1 ciphertext: 
`Ctxt1 = [0, 2, 6, 8, -1, X, X, ...]`, where `X` indicates a don't-care value.

### Hybrid-based packing
In this example we want to find the words "he", "ll", "wo", "rd", "no" in the text "hello world"

The executable will be run as follows:
```
./app --cc cc.bin --key_public pub.bin --key_mult mult.bin --input in_hyb.bin --word_size 5,5 --output out.bin --text "hello world"
```

The file `in_hyb.bin` will include a TileTensor with 1 ciphertext (see HElayers documentation about TileTensors and their shapes) with shape [5/8, 2/2] (this example assumes a ciphertext size of 16 slots. For 32K slots the shape will be different).

`ctxt1 = ['h', 'l', 'w', 'r', 'n', 0, 0, 0, 'e', 'l', 'o', 'd', 'o', 0, 0, 0, ...]` 
(the noise added by CKKS during encryption is not shown).

An example output for this input will be a TileTensor with 1 ciphertext: 
`Ctxt1 = [0, 2, 6, 8, -1, X, X, ...]`, 
where `X` indicates a don't-care value.

Note that in hybrid packing you can ask for the input TileTensor to have a different shape as well.

## Evaluation Criteria
Submissions will be evaluated on these testcases:

|text size | number of strings | max. string size | 
|----------|-----------------|---------------| 
|65,500    | 1               | 65,450
|100       | 500             | 90
|1,000,000 | 80              | 999,000
|1,000,000 | 800             | 999,900
|1,000,000 | 1               |  4


1.  **Correctness and accuracy:**  The output of the program for valid input (i.e., numbers in the range  $[0,255]$)  **must**  be correctly the indexes of the input words in the text. The output may have an error of no more than $0.4$ for each element.
2.  **Execution time:**  The cumulative running time of the application on the provided input data.

That is, the winner will be the fastest application whose output is correct and accurate.

## Scoring & Awards

The winner will be awarded  **$4000**.

## Challenge Committee

-   [Gurgen Arakelov](https://www.linkedin.com/in/gurgen-arakelov-943172b9/), Fair Math
-   [Sergey Gomenyuk](https://www.linkedin.com/in/sergey-gomenyuk-7a355a42/), Fair Math 
-   [Yuriy Polyakov](https://www.linkedin.com/in/yuriy-polyakov-796b84a/), Duality 
-   [Hayim Shaul](https://www.linkedin.com/in/hayim-shaul-b2658/), IBM Research

## Useful Links

### FHE

-   [FHERMA participation guide](https://fherma.io/how_it_works)—more about FHERMA challenges.
-   A vast collection of resources collected by  [FHE.org](http://fhe.org/)  [https://fhe.org/resources](https://fhe.org/resources), including tutorials and walk-throughs, use-cases and demos.
-   [OpenFHE AAAI 2024 Tutorial](https://openfheorg.github.io/aaai-2024-lab-materials/)—Fully Homomorphic Encryption for Privacy-Preserving Machine Learning Using the OpenFHE Library.

### NDFA Methods Studied Under FHE
- Genise, N., Gentry, C., Halevi, S., Li, B., Micciancio, D. (2019). Homomorphic Encryption for Finite Automata. In: Galbraith, S., Moriai, S. (eds) Advances in Cryptology – ASIACRYPT 2019. ASIACRYPT 2019. Lecture Notes in Computer Science(), vol 11922. Springer, Cham. https://doi.org/10.1007/978-3-030-34621-8_17

- Charlotte Bonte and Ilia Iliashenko. 2020. Homomorphic String Search with Constant Multiplicative Depth. In Proceedings of the 2020 ACM SIGSAC Conference on Cloud Computing Security Workshop (CCSW'20). Association for Computing Machinery, New York, NY, USA, 105–117. https://doi.org/10.1145/3411495.3421361

## Help

If you have any questions, you can:

-   Contact us by email:  [support@fherma.io](mailto:support@fherma.io)
-   Join our  [Discord](https://discord.gg/NfhXwyr9M5)  server, and ask your questions in the  [#fherma channel](https://discord.com/channels/1163764915803279360/1167875954392187030).
-   Open an issue in the  [GitHub Repository](https://github.com/Fherma-challenges/parity).
-   Use  [OpenFHE Discourse](https://openfhe.discourse.group/)  for OpenFHE related issues.
