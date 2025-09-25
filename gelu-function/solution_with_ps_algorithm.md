# GELU Approximation in FHE with the Paterson–Stockmeyer Algorithm

> The article details the solution provided by the winner of the GELU Function challenge.

**Authors:** Seunghun Paik (Hanyang University, South Korea), Nirajan Koirala (University of Notre Dame, USA)

## 1) Problem & Target 

We need an FHE-friendly approximation of the tanh-form GELU

<p align="center">
  <span style="font-size: 1.3em;">
    GELU<sub>tanh</sub>(x) = (1/2)x(1 + tanh( √(2/π) · (x + 0.044715x<sup>3</sup>) ))
  </span>
</p>

with uniform error &le; 10<sup>-3</sup> over `[-7, 7]` (we use `[-8, 8]` in
practice for an integer scaling trick; see §5.1). Input data is a
4096-dimensional vector, randomly generated within the range `[-7, 7]`
and normally distributed.

We target a small multiplicative depth so that no bootstrapping is
required. We minimize the number of ciphertext multiplications,
preferring squarings and constant multiplications instead. To ensure
stable numerics, we work in the Chebyshev basis on the interval `[-1,1]`
and carefully align CKKS levels and scales throughout the evaluation.
The implementation is fully batchable, supporting slot-wise CKKS
evaluation for `4096`-dimensional vectors.

## 2) Key Observation & Approximation Strategy 

First, we observe that the GELU function can be written as a summation
of `(1/2)x` and the remaining even function. From this, we attempted to
approximate the even part only; namely, we can approximate

<p align="center">
  <span style="font-size: 1.3em; border: 1px solid #000; padding: 4px;">
    GELU(x) ≈ (1/2)x + P<sub>even</sub>(x/8)
  </span>
</p>

- P<sub>even</sub>(z) is an even Chebyshev polynomial on `[-1, 1]`.
- Using `x/8` puts the domain into `[-1, 1]`, where Chebyshev expansions are numerically stable.
- Adding `(1/2)x` finally recovers the GELU without additional errors.

This is efficient in FHE because even Chebyshev terms are built from
squarings only plus a few products. We approximate the tanh-form GELU on
a bounded range by exploiting its symmetry.
P<sub>even</sub> is an even polynomial. The `x → x/8` rescaling puts the input in `[-1, 1]` so Chebyshev polynomials are the natural basis.  Next, we can construct Chebyshev basis functions T<sub>0</sub>, …, T<sub>24</sub> and enforce evenness by zeroing all odd coefficients.


Our next key idea is to use a two-step coefficient estimation using the
following:

- (Step 1) Usual Chebyshev fit (initializer): Start from a standard
  Chebyshev approximation on `[-1, 1]` to get a good initial
  coefficient vector.

- (Step 2) L<sub>∞</sub> fine-tuning with gradient descent: Treat the coefficients as learnable parameters and refine them by minimizing the max absolute error (an L<sub>∞</sub> objective) between (1/2)x + P<sub>even</sub>(x/8) and the PyTorch reference GELU approximation (`gelu(., approximate="tanh")`) on a dense grid of x ∈ `[-8, 8]`. We apply early stopping triggers once the uniform error drops below the target (i.e., 10<sup>-3</sup>).


Using the above procedure, we found that the following degree-24 even
polynomial is suitable for obtaining the desired accuracy level required
for the task. We provide the exact coefficients of the polynomial from
the lowest to the highest degree as follows:

```cpp
[5.052839140598564, 0.0, 1.7359793098548242, 0.0, -0.3726023812500432,
0.0, 0.17095326369135477, 0.0, -0.09757261019185769, 0.0,
0.060092112307910166, 0.0, -0.03731996858905697, 0.0,
0.022792097220090873, 0.0, -0.013309648347659766, 0.0,
0.007610728279999343, 0.0, -0.004196815886808643, 0.0,
0.00215229898578225, 0.0, -0.0012773772058335409]
```


These coefficients feed directly into the low-depth Chebyshev evaluation
schedule used in the FHE implementation, where the final approximant is
(1/2)x + P<sub>even</sub>(x/8). We also visualize the
approximation error using the above coefficients in Figure 1.

<p align="center">
  <img src="https://d2lkyury6zu01n.cloudfront.net/images/approxGELU.png" width="400"/>
  <br>
  <em>Figure 1: Approximation error for GELU using our approach (blue lines)</em>
</p>

## 3) Evaluating the Polynomial in FHE 

After finding an approximation polynomial, we evaluate it via the
Paterson-Stockmeyer (PS) algorithm. Note that for even polynomials, we
can reduce the number of operations by considering coefficients with
even degree only. In the PS algorithm, we need to schedule how to
recursively divide the polynomial in the form of
`f(X) = q(X)g(X) + r(X)` and evaluate the resulting polynomials using
pre-computed powers at the end.

We first factor the degree-24 even series into a block form that is inexpensive under FHE. We can write:

<p align="center">
  <span style="font-size: 1.1em;">
    P<sub>even</sub>(z) = c<sub>24</sub>T<sub>24</sub>(z) + f<sub>1</sub>(z)T<sub>16</sub>(z) + f<sub>2</sub>(z)T<sub>8</sub>(z) + f<sub>3</sub>(z)
  </span>
</p>

where f<sub>1</sub>, f<sub>2</sub>, f<sub>3</sub> are polynomials of degree at most 6, and T<sub>i</sub> is the Chebyshev basis polynomial of degree i.  With precomputation of T<sub>2</sub>, T<sub>4</sub>, T<sub>6</sub>, T<sub>8</sub>, T<sub>16</sub>, T<sub>24</sub>, we simply express the idea of the PS algorithm in Chebyshev blocks, which maps more transparently to squarings and a few products under CKKS.


This is the final solution in FHE (using OpenFHE) after incorporating all the above ideas:

1. **Scale input:** `EvalMultInPlace(x, 0.125)` ⇒ z = x/8.

2. **Build nodes:**
   - x<sub>2</sub> = 2z<sup>2</sup> − 1,  
     x<sub>4</sub> = 2x<sub>2</sub><sup>2</sup> − 1,  
     x<sub>6</sub> = 2x<sub>2</sub> · x<sub>4</sub> − x<sub>2</sub>,  

   - x<sub>8</sub> = 2x<sub>4</sub><sup>2</sup> − 1,  
     x<sub>16</sub> = 2x<sub>8</sub><sup>2</sup> − 1,  

   - T<sub>24</sub> via 2x<sub>16</sub> · x<sub>8</sub> − x<sub>8</sub> (one product)

3. **Small affine combos:** v1, v2, v3 = linear forms in {x<sub>2</sub>, x<sub>4</sub>, x<sub>6</sub>} (+ constants).

4. **Compose blocks:** multiply v2 by T<sub>8</sub> and v3 by T<sub>16</sub>, add the T<sub>24</sub> term.

5. **Add (1/2)x:** multiply the original z by 4 (giving (1/2)x) and add to the polynomial output.

6. **Level alignment:** `AdjustLevelsAndDepthInPlace(...)` is used before mixed products to keep scales compatible in CKKS.


## 4) Complexity & Depth Consumption 

For node construction, we require one ciphertext multiplication to form T<sub>6</sub> and one to obtain T<sub>24</sub> via 2T<sub>16</sub>T<sub>8</sub> − T<sub>8</sub>.  For composition, two additional products are needed when combining blocks with T<sub>8</sub> and T<sub>16</sub>.  In total, the circuit uses approximately **four ciphertext multiplications**, plus 4–5 squarings.  The effective multiplicative depth is about **5 (at most 6)**, depending on the rescaling values used in CKKS within OpenFHE.  Constant multiplications and additions are inexpensive in CKKS and have minimal impact on the overall cost.  No slot rotations are required.


## 5) Some Optimization Tricks 

We also provide some optimization tricks to reduce the required depth
for FHE.

### 5.1) Dealing with Range `[-8,8]` instead of `[-7,7]`

When starting polynomial evaluation with a Chebyshev basis, we first need to normalize the input by dividing its range; in our case, we need to compute `x ← x/7` first.  Here, since we first substitute `y = 0.5x` and proceed with the remaining operations, we can first substitute `y = x/7`, do a polynomial evaluation at the latter part, and add `3.5y` at the end, serving the role of `0.5x`.  Here, if we use the range `[-8, 8]` instead, then a cheaper integer multiplication, `4y`, is sufficient instead of the floating-point multiplication, `3.5y`.  Note that the polynomial we found still provides an accurate approximation even when we increase the range to `[-8, 8]`.



### 5.2) Note on Computing c<sub>24</sub>T<sub>24</sub>(X)  

If we compute T<sub>24</sub>(X) from scratch, then it requires depth `5` computation from computing T<sub>16</sub>(X) and doing a degree-1 computation with T<sub>8</sub>(X).  Hence, if we further multiply c<sub>24</sub> at the end, since c<sub>24</sub> is a real-valued number, the final required depth becomes `6`.  To reduce the depth from this last step, we first multiply c<sub>24</sub> by T<sub>8</sub>(X) and then run a degree-1 computation with T<sub>16</sub>(X) in accordance with the definition of the Chebyshev basis.  Note that computing T<sub>8</sub>(X) consumes `3` depths, so both of c<sub>24</sub>T<sub>8</sub>(X) and T<sub>16</sub>(X) take depth `4`.  Hence, we can obtain c<sub>24</sub>T<sub>16</sub>(X) via depth `5` computation.


### 5.3) Managing Levels during the PS Algorithm 
In CKKS, the unit cost per operation becomes cheaper as we proceed with the computation; internally, CKKS applies modulus switching for each non-integer multiplication, reducing the ciphertext modulus.  When computing f(X) via the PS algorithm, especially for f<sub>1</sub>(X), f<sub>2</sub>(X), f<sub>3</sub>(X), we can observe that each Chebyshev basis has a different level.  Hence, we can apply modulus switching on T<sub>2</sub>(X) and T<sub>4</sub>(X) before computing f<sub>1</sub>(X), f<sub>2</sub>(X), f<sub>3</sub>(X) so they have the same level as T<sub>6</sub>(X).