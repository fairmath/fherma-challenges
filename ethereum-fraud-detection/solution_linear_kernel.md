# Ethereum Fraud Detection via SVM with Linear Kernel

*The article details the solution provided by the winner of the [Ethereum Fraud Detection via SVM challenge](https://fherma.io/challenges/66e8180996829cc963805ffb/overview).*

**Author:** [Chi-Hieu Nguyen](https://www.linkedin.com/in/hieu-nguyen-ba6548316), University of Technology Sydney, Australia.

## Introduction

The challenge requires training a SVM model on a public clear-text dataset for Ethereum fraud detection, then evaluating it on a private encrypted test set using HE. The goal is to classify transactions as fraudulent or legitimate while preserving data privacy during inference. SVMs are well-suited for HE-based inference due to their reliance on a decision function that can often be simplified to a linear operation (e.g., a dot product for linear kernels).
    
## Data Preprocessing

The public training dataset contains Ethereum transaction features for fraud detection. We analyzed feature skewness using `scipy.stats.skew`, revealing high skewness (>1) across all columns, indicating non-normal distributions.
    
```python
                                               Column   Skewness
0                                  ERC20 avg val sent  88.696538
1                                  ERC20 max val sent  88.682094
2                                  ERC20 min val sent  88.679603
3                                   ERC20 max val rec  88.631605
4                          ERC20 total Ether received  88.608206
5                              ERC20 total ether sent  88.576675
6                                    avg val received  86.632342
7                                        min val sent  76.084382
8                          min value sent to contract  71.400808
9                            max val sent to contract  70.506146
10                         total ether sent contracts  70.506005
...
36  total transactions (including tnx to create co...   6.797555
37            Time Diff between first and last (Mins)   1.802201
```

High skewness suggests that features are heavily tailed, which can degrade SVM performance by causing numerical instability or poor separation of classes. Transforming features to a logarithmic scale reduces skewness, making the data more symmetric and closer to a normal distribution. This ultimately boosts classification accuracy.

Since the dataset includes negative values, we first apply `MinMaxScaler` to scale features to [0, 1], then use a polynomial approximation of the logarithm (`poly_log`) to enable HE-compatible evaluation.

```python
scaler = MinMaxScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)
X_train = poly_log(X_train)
X_test = poly_log(X_test)
```
    
The `poly_log` function approximates the logarithm over [0.0001, 1] using Chebyshev interpolation with degree 121 for high precision:
    
```python
x = np.linspace(0.0001, 1, 10000)
y = np.log(x)
poly_log = C.Chebyshev.fit(x, y, 121)
```
    
After log transformation, we apply a second `MinMaxScaler` to rescale the data back to [0, 1].
    
```python
scaler2 = MinMaxScaler()
X_train = scaler2.fit_transform(X_train)
X_test = scaler2.transform(X_test)
```
    
![log](https://d2lkyury6zu01n.cloudfront.net/images/hita-fraud-detection-pic1.png)
***Figure 1**: Illustration of the log approximation.*
    
## Model Training
    
We implement the SVM using `sklearn.svm.SVC` and tune hyperparameters `C` and `gamma` with GridSearchCV.
    
```python
tuned_parameters = [
    { "gamma": [1,0.1,0.01,0.001], "C": [1, 10, 100, 1000]},
]
grid = GridSearchCV(SVC(kernel='linear'), tuned_parameters, refit=True, cv=5, scoring='f1')
grid.fit(X_train, y_train)
```

We select the linear kernel for its simplicity and HE compatibility. Non-linear kernels (e.g., RBF, polynomial) could improve accuracy but introduce significant complexity in HE. They require evaluating the kernel function over potentially hundreds of support vectors, involving costly operations like rotations. In contrast, the linear kernel’s decision function is a single dot product between the input vector and the model’s weights, enabling faster and more efficient HE inference.
    
The grid search yields an F1 score of 0.9025 on the training set. Validation on a separate clear-text test set achieves an F1 score of 0.9161, confirming robust generalization.
    
```python
print("Train F1 Score :",grid.best_score_)
best_y_pr = grid.predict(X_test)
print('Test F1 Score: ', f1_score(y_test, best_y_pr))
    
Output:
Train F1 Score : 0.9025388783902716
Test F1 Score:  0.9161290322580645
```
    
## HE Implementation
    
For HE inference, we use the CKKS scheme to evaluate the trained SVM on encrypted inputs. The process mirrors preprocessing and model evaluation in the clear-text domain but operates on ciphertexts.

First, we apply the `MinMaxScaler` and `poly_log` transformation to the input ciphertext:
    
```cpp
// Extract attributes from the first MinMaxScaler, where scale_1 = scaler.scale_ and min_1 = scaler.min_
m_OutputC = m_cc->EvalMult(m_OutputC, m_cc->MakeCKKSPackedPlaintext(scale_1));
m_cc->EvalAddInPlace(m_OutputC, m_cc->MakeCKKSPackedPlaintext(min_1));
    
m_OutputC = m_cc->EvalChebyshevSeries(m_OutputC, poly_cheb, 0.0001, 1);
    
// Similarly, we have scale_2 = scaler2.scale_ and min_2 = scaler2.min_
// However, this second scaling can be skipped as discussed below
// m_OutputC = m_cc->EvalMult(m_OutputC, m_cc->MakeCKKSPackedPlaintext(scale_2));
// m_cc->EvalAddInPlace(m_OutputC, m_cc->MakeCKKSPackedPlaintext(min_2));
```

To optimize, we skip the second scaling (`scaler2`) by fusing it with the SVM weight multiplication, reducing the multiplication depth. We adjust the model’s weights and bias accordingly:
    
```python
w = grid.best_estimator_.coef_[0]
b = grid.best_estimator_.intercept_[0] + (scaler2.min_ * w).sum()
w = w * scaler2.scale_
```
    
The HE evaluation computes the decision function as a dot product:
    
```cpp
m_OutputC = m_cc->EvalMult(m_OutputC, m_cc->MakeCKKSPackedPlaintext(w));
int k = 64;
while (k > 1) {
    k = k/2;
    m_OutputC = m_cc->EvalAdd(m_OutputC, m_cc->EvalRotate(m_OutputC, k));
}
m_OutputC = m_cc->EvalAdd(m_OutputC, b);
```

This accumulates the dot product result in the first slot of the ciphertext. To obtain the predicted label, we compute the sign of this value. We scale the first slot to [-1, 1], mask other slots containing dummy values to avoid overflow, and apply an approximated sign function using three composite polynomials (each degree 25):
    
```cpp
std::vector<double> mask(32768);
mask[0] = 0.01; // Scale to [-1, 1]
m_OutputC = m_cc->EvalMult(m_OutputC, m_cc->MakeCKKSPackedPlaintext(mask));
    
m_OutputC = m_cc->EvalChebyshevSeries(m_OutputC, sign_poly_1, -1, 1);
m_OutputC = m_cc->EvalChebyshevSeries(m_OutputC, sign_poly_2, -1, 1);
m_OutputC = m_cc->EvalChebyshevSeries(m_OutputC, sign_poly_3, -1, 1);
```
This produces the final encrypted classification label (1 for fraud, -1 for legitimate).
    
## Conclusion

The solution achieves high accuracy (F1 > 0.91) on the Ethereum fraud detection task while enabling secure inference on encrypted data with a processing delay of approximately 11 seconds per inference. By leveraging a linear SVM, Chebyshev polynomial approximations, and optimized HE operations, we balance performance and computational efficiency.