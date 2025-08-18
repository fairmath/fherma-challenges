# Sentiment Analysis

*The article details the solution provided by the winner of the [FHERMA](https://fherma.io) [Sentiment Analysis challenge](https://fherma.io/challenges/681b3ff2da06abf28988891d).*

**Author:** [Chi-Hieu Nguyen](https://www.linkedin.com/in/hieu-nguyen-ba6548316), University of Technology Sydney, Australia.

## Introduction

This challenge aims at developing a HE-enabled classifier for NLP tasks, namely to predict the sentiment polarity (positive, negative, or neutral) of an encrypted query vector derived from a user tweet. Participants are provided with a non-encrypted training dataset to train a multiclass classification model. The trained model is then adapted for privacy-preserving inference, enabling prediction on encrypted inputs from a private test set.

## Model Selection

We first implemented a 3-layer MLP classifier as a baseline, achieving an F1-score of approximately 75%. However, MLPs involve multiple vector-matrix multiplications and non-linear activation functions, which can result in high computational overhead when adapted for HE operations. As an alternative, we explored the ChebyKAN architecture, previously applied in our winning solution to the [House Price Prediction Challenge](https://fherma.io/content/682c2c423e4a37c9c28266c6). ChebyKAN employs per-edge learnable Chebyshev polynomial activations, making it more HE-friendly and parameter-efficient compared to traditional MLPs. Although KAN architectures are generally reported to underperform MLPs in various ML and NLP tasks [1], our experiments demonstrated comparable performance between ChebyKAN and the baseline MLP. Given its lower HE computational cost, we selected ChebyKAN as our final model.


## Model Architecture

We trained a 2-layer ChebyKAN with the following components:
* **Input Normalization:** A min-max scaler maps input features to the range [-0.8, 0.8] (instead of the standard [-1, 1]) to provide a safety margin, preventing overflow when processing unseen test samples during encrypted inference.
* **First Layer:** Transforms the normalized inputs into a hidden representation by computing weighted sums of Chebyshev polynomials.
* **Activation:** Applies a scaled hyperbolic tangent activation ($0.9\tanh(\cdot)$) to constrain outputs within [-0.9, 0.9], ensuring numerical stability and preventing overflow .
* **Second Layer:** Aggregates the hidden representations to generate the final price prediction using Chebyshev-based polynomial transformation.


## Hyperparameter tuning

We performed a grid search over polynomial degrees (ranging from 3 to 5) and hidden layer sizes (8, 16, 32, 64) to maximize the F1-score on validation set. A configuration with 16 hidden units and a polynomial degree of 3 for both layers achieved an F1-score of above 75%, slightly surpassing the 3-layer MLP baseline. Additionally, this setup maintains a low multiplication depth of 2 levels per layer, ensuring efficient HE inference.

## Implementation

The ChebyKAN inference procedure was implemented following the same method described in our [House Price Prediction solution](https://fherma.io/content/682c2c423e4a37c9c28266c6).

## References

[1] Yu, Runpeng, Weihao Yu, and Xinchao Wang. *Kan or mlp: A fairer comparison*. arXiv preprint arXiv:2407.16674 (2024).