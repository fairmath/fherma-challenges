# Fraud Detection on Ethereum Using Homomorphic SVM with RBF Kernel

*The article details the solution provided by the winner of the [Ethereum Fraud Detection via SVM challenge](https://fherma.io/challenges/66e8180996829cc963805ffb/overview).*

**Author:** Victor Correa

## Model Training
For fraud detection on Ethereum transactions, a **Support Vector Machine (SVM)** with a **Radial Basis Function (RBF) kernel** was selected due to its superior performance in capturing complex, non-linear patterns in transaction data. The RBF kernel is defined as:  

$$
K(x, x_i) = \exp\left(-\gamma \|x - x_i\|^2\right)
$$

### Optimal Hyperparameters
- **Kernel Coefficient (γ):** `0.5`  
- **Regularization (C):** `1200`  
- **Number of Support Vectors:** `512`  

This configuration resulted in the highest observed F1-score. Despite the numerous features and support vectors, the **SIMD (Single Instruction, Multiple Data)** capabilities of **CKKS homomorphic encryption** ensured minimal computational overhead.

## Homomorphic Inference
The SVM decision function is computed as:  

$$
f(x) = \text{sign}\left(\sum_{i=1}^n y_i K(x, x_i) + b\right)
$$

Where:
- The Ethereum transaction feature vector x is **encrypted**
- Support vectors \( x_i \), dual coeffs \( y_i \) and bias \( b \) are in **clear**

## Key Challenges & Solutions
1. **Non-Polynomial Kernel Approximation**  
   - The RBF kernel is non-polynomial and cannot be directly evaluated in **CKKS**.  
   - **Solution:** A polynomial approximation over the interval **[-30000, 0]** with a **degree-1024 polynomial** was employed to ensure high precision.

2. **Sign Function Approximation**  
   - The **sign** function is discontinous and must be approximated.  
   - **Practical approximation:** Polynomial approximation of the **hyperbolic tangent (tanh) approximation** with:  
     - **Polynomial Degree:** `256`  
     - **Approximation Interval:** `[-70, 70]`  
     - **Sharpness Parameter (α):** `6` (higher α improves approximation to sign but must be chosen with respect to the degree)  

 3. **Efficient SIMD Packing**
    - SIMD batching allows to parallelize kernel evaluations, significantly reducing latency in encrypted inference. Specifically, the 64 features of the 512 support vectors can fit int 64×512=32684 slots, taking full advantage of the available plaintext capacity. Each block of 64 slots computed the kernel between the encrypted transaction and a support vector.

## SIMD Inference Steps

The following outlines the key SIMD inference steps involved in efficiently computing the final prediction:
- SIMD squaring of feature differences
- Local summation to compute squared distances
- Kernel evaluation for each computed distance
- SIMD multiplication of kernels with dual coefficients
- Global summation across relevant slots, followed by bias addition
- Homomorphic sign approximation for the final prediction

## Implementation with OpenFHE

All polynomial approximations and evaluations were performed using the OpenFHE library’s `EvalChebyshevFunction` method. The approximation intervals were selected taking into account the outputs of the decision function on the training dataset.