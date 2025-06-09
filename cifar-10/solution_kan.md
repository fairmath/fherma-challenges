# Privacy-Preserving CIFAR-10 Classification Using KAN

*The article details the solution provided by the winner of the [CIFAR-10 Image Classification challenge](https://fherma.io/challenges/652bf663485c878710fd0209).*

**Author:** [Chi-Hieu Nguyen](https://www.linkedin.com/in/hieu-nguyen-ba6548316), University of Technology Sydney, Australia.

## Introduction

The challenge task involves inferring the class of an encrypted input image, a problem situated within the domain of privacy-preserving machine learning inference. This area has recently garnered significant interest from both academia and industry. The challenge is based on a public dataset, allowing unrestricted use of training data. Consequently, one could attempt to overfit a machine learning model on the entire set of 60,000 CIFAR images (comprising 50,000 training images and 10,000 testing images) to achieve optimal accuracy. This important point makes public implementations of HE image classification, which are based on conventional neural networks (e.g., CNN, ResNet), too complex to be directly used as a competitive solution.

## Model Selection

We experimented with various neural network architectures and ultimately decided to use the Kolmogorov-Arnold Network (KAN). Compared to traditional multilayer perceptron networks, KAN requires fewer model parameters and performs well in signal/function regression or interpolation tasks, making it well-suited for this challenge. To enhance evaluation efficiency, we adopted a variant of KAN based on Chebyshev polynomials, known as ChebyKAN [1]. The Chebyshev basis can be efficiently computed using recursive formulas, thereby reducing computational costs and minimizing ciphertext level consumption.

## Model Training

We trained a KAN network with a single layer of learnable activation functions. To optimize runtime, we sought the lowest possible activation degree that could still achieve 100% prediction accuracy. The training code was adapted from a GitHub repository [1]. We successfully trained the model to a degree of 8, which required a multiplication depth of 5: one for normalizing the input vector and four for evaluating the Chebyshev polynomials.

## Optimization

Given that the input vector consists of 3,072 elements (from a 32x32 image with three channels), the minimum ring dimension we could use in the challenge was 8,192, with up to 4,096 plaintext slots to encrypt the entire input vector. We aimed to work with this lowest ring dimension to minimize complexity and maximize computation speed.

We observed that the dominant HE operator during inference was the rotation operator, which necessitates costly key-switching calculations. Theoretically, to compute the sum over a vector of $N$ elements packed in a single ciphertext, one must perform $\log_2(N)$ rotations using the folding technique. With an input dimension of 3,072 and an output dimension of 10 classes, the first layer's forward pass (calculating 10 different summations for the 10 classes) would require at least $\left \lceil\log_2(3,072)\right \rceil + 10 - 1 = 21$ rotations at a ring dimension of 8,192. To reduce this number and expedite the inference process, our idea is to infer the probability for each output class based on subsampled portions of the input image.

Specifically, the output probability for the $i$-th class was computed from pixels located at indices $i + 10j$, where $j = 0, 1, \ldots, 306$, in the flattened input vector, as illustrated in Figure 1. In this manner, the output probability of a class can be viewed as a function interpolation task over approximately 307 pixels of the input image. Calculating the sum over these subsets of evenly-spaced pixels can be optimally achieved using $\left \lceil\log_2(307)\right \rceil = 9$ rotations in total.

![CIFAR10-Page-1](https://hackmd.io/_uploads/BJ9PL0JCA.png)

***Figure 1**: Pixel selection for efficient class probability computation.*

However, reducing the number of input dimensions also decreases accuracy, potentially falling below the acceptable threshold. To counteract this, we used multiple fragmented pixels at different offsets to predict class probabilities. Specifically, the probability for the $i$-th class was associated with pixels at positions $i + 10j + \text{offset}$, with $j = 0,\ldots, 306$ and $\text{offset} = 0, \ldots, n_{\text{offset}}$ (Figure 2). A higher $n_{\text{offset}}$ value results in higher prediction accuracy. By experimentally varying $n_{\text{offset}}$, we selected the lowest value yielding over 85% accuracy, which was $n_{\text{offset}} = 3$ for the time-oriented track, and the lowest value achieving 100% accuracy, which was $n_{\text{offset}} = 5$ for the accuracy-oriented track. Consequently, the number of rotation operations required for each track was $\left \lceil\log_2(3 \times 307)\right \rceil + 3 -1 = 12$ and $\left \lceil\log_2(5 \times 307)\right \rceil + 5 -1 = 15$, respectively. By minimizing the number of required rotations, our approach significantly accelerates processing speed compared to other solutions that operate on the full image.

![CIFAR10-Page-2](https://hackmd.io/_uploads/BJL-vRJAR.png)

***Figure 2**: Pixel selection with different offsets ($n_{\text{offset}} = 3$) for enhanced class probability computation.*

## References

[1] https://github.com/SynodicMonth/ChebyKAN