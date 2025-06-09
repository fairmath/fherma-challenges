# Encrypted Lookup Table

*The article details the solution provided by the winner of the [Lookup Table challenge](https://fherma.io/challenges/665efcf8bad7bdd77d182111)*

Author: [Jules Dumezy](https://www.linkedin.com/in/jules-dumezy/), MSc Student at the Ecole Centrale de Lille.

## Introduction

A lookup table, specifically `A[i]` for a list `A` and an index `i`, is a fundamental concept in computer science and plays a vital role in efficient algorithm design and implementation. At their core, LUTs provide a mechanism for efficiently retrieving precomputed values based on an index, thereby allowing for constant-time access to data, which is crucial for performance-critical applications.

Aside from the obvious use of LUT to retrieve data and use it in calculation, it can also be used to evaluate an arbitrary function `f`. By precomputing its outputs and storing them in an encrypted vector, `f`'s computation can be reduced to a simple lookup operation, which can be far less resource-intensive. This capability can be essential in applications such as encrypted neural networks, and allows to easily evaluate non-smooth functions.


## The challenge

We are working with BFV using the plaintext modulus 65537. Given an encrypted vector $A = [x_0,\dots,x_{n-1}]$ of size 2048 and an encrypted index $i\in [0..n-1]$, we want to extract $x_i$. Specifically, we want to obtain an encrypted vector with $x_i$ in the first slot.

Although the challenge specifies that the values $x_i$ are bounded between 0 and 255, the proposed solution does not rely on this restriction. Additionally, the solution can be easily adapted for larger vectors (with more than 2048 values) or for larger plaintext moduli.

## The algorithm

The algorithm can be divided into two main steps :

1. Creating a mask vector with a $1$ at the $i$-th element and zeros everywhere else
2. Extracting the value from $A$ and placing it in the first slot

### Step 1

Since we use packing, the encrypted index vector has the following form: $[i, 0, 0, 0,\dots, 0]$.
We start by rotating this vector by -2047, resulting in a vector with 2047 zeros and the index $i$ at the 2048th position (index 2047).

This approach is used because rotations are generally faster with positive values, and it also minimizes the number of rotation keys required—we only need 12 rotation keys in total by reusing them, instead of 22.

By applying 11 rotations and additions (using rotation keys 1, 2, 4, 8, ..., 1024), we obtain a new encrypted vector $c_1$ with $i$ in the first $2048$ slots $[i, i, i,\dots, i, 0, \dots, 0]$.

Next we create a packed plaintext for the vector $[0, -1, -2, -3, \dots, -2045, -2046, -2047]$.
We then add this plaintext to the previous ciphertext $c_1$ to produce a new ciphertext $c_2$ of the form $[i, i-1, i-2, \dots, i-2047]$. This new ciphertext $c_2$ has exactly one zero at the $i$-th slot, with non-zero values in every other slot.

By Fermat's Little Theorem, and because operations are performed modulo $65537 = 2^{16}+1$ (a prime number), we know that for all $x\in[1, 65536]$, $x^{65537-1} = x^{2^{16}} = 1$.

Using fast exponentiation, we only need 16 multiplications to exponentiate each value of $c_2$ to $2^{16}$, creating $c_3$, a ciphertext containing ones in all $2048$ slots except for $i$-th slot, since $0^{65536} = 0$.

Finally, we create a packed plaintext filled with ones, and subtract $c_3$ from it, giving us the desired mask vector $m$ with zeros everywhere except for the $i$-th slot.

### Step 2

Given the mask vector $m$ and the original encrypted vector $A$, we use a seventeenth multiplication to multiply $m$ by $A$, resulting in the partial result ciphertext $c_4$: $[0, \dots, 0, x_i, 0,\dots, 0]$.

Knowing that $x_i$ is in the first $2048$ slots, we apply the same strategy of $11$ rotations and additions (with the same rotation keys) to bring $x_i$ to the first slot.

## References

[1] **Ilia Iliashenko and Vincent Zucca**, "Faster homomorphic comparison operations for BGV and BFV". Cryptology ePrint Archive, Paper 2021/315, 2021. Available online at https://eprint.iacr.org/2021/315
