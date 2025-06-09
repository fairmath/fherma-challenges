# Privacy-Preserving CIFAR-10 Classification Using MLP

*The article details the solution provided by the winners of the [CIFAR-10 Image Classification challenge](https://fherma.io/challenges/652bf663485c878710fd0209), LattiGo implementation.*

Authors: [Valentina Kononova](https://ru.linkedin.com/in/valentina-kononova-a9a23b180), [Dmitry Tronin (aka osmenojka)](https://www.linkedin.com/in/dmitry-tronin-28438b85/) and Dmitrii Lekomtsev.

## Overview of the challenge

The challenge involved classifying CIFAR-10 images encrypted using the CKKS homomorphic encryption scheme. The goal was to efficiently predict the labels without decrypting the data. This challenge presented a unique opportunity to explore the intersection of cryptography and machine learning, specifically in the context of privacy-preserving computations. 

It's important to note that strong generalization capability was not necessarily required for this challenge, allowing us to overfit the model entirely on the provided data.

## Model and training process

Initially, we experimented with the ResNet architecture, however, given the nature of this particular challenge, we opted for a significantly simpler neural network model.

### Neural network architecture

The chosen neural network model had the following architecture:
- **Input Layer**: $3072$ neurons (corresponding to the `32x32x3` CIFAR-10 images).
- **Hidden Layer**: $16$ neurons.
- **Output Layer**: $10$ neurons (one for each CIFAR-10 class).

This configuration resulted in approximately $50000$ parameters.

### Training procedure

To achieve $100$% accuracy, we trained the model twice, each time using a different activation function to avoid local minimum issues:

1. During the **first training phase**, we used a cubic activation function to improve neural network convergence.
2. On the **second phase**, we continued training with a quadratic activation function. This allowed us to reduce the multiplication depth and, therefore, speed up the calculations.

The training was conducted using the `PyTorch` library. Training with the cubic activation function took one day, followed by two additional days of training with the quadratic activation function.

### Loss function and optimizer

We utilized the cross-entropy as our loss function and the L-BFGS optimizer for training.

* **Cross-entropy**, also known as logarithmic loss or log loss, is widely used in classification problems to measure the performance of a model.
* **L-BFGS** is a quasi-Newton method that approximates the Broyden–Fletcher–Goldfarb–Shanno (BFGS) algorithm using limited computer memory. It iteratively improves an estimate of the inverse Hessian matrix and uses it to compute search directions.

These choices were made based on their compatibility with the nature of our problem and demonstrated higher accuracy with faster convergence compared to gradient methods.

### Model deployment

The model weights were exported in JSON format for use in a Go application.

## Operations on encrypted data

Given the encrypted nature of the data, certain operations had to be implemented manually due to the the eval sum key has not been generated:
* **EvalSum** - custom implementation since sum keys were not provided.
* **DotProduct** - custom implementation of EvalInnerProduct was necessary for encrypted operations.

## Optimizations

Normally, neural networks parallelize well, but Python's pickle serialization limitations hindered initial attempts to accelerate computations through parallelism. However, employing goroutines in Go and the LattiGo library, we managed to speed up execution by at least three times!

Additionally, we had to fix a few bugs in the code and implemented unit, integration, and performance tests to be able to record necessary data and compare solutions efficiently.

Eventually, we reduced the number of multiplications, adjusted the parameters `log_q` and `log_n`, applied parallelism in Go, and managed to accelerate performance by an additional $30$%. 

## Conclusion

This challenge showcased the feasibility of using simple neural network architectures and custom implementations to handle operations on homomorphically encrypted data, ultimately achieving high accuracy in classification tasks.
