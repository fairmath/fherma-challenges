# Sentiment Analysis using Multinomial Logistic Regression

*The article details the solution provided by the winner of the [Sentiment Analysis challenge](https://fherma.io/challenges/681b3ff2da06abf28988891d).*

**Author:** [Strahinja Praška](https://www.linkedin.com/in/strahinja-pra%C5%A1ka-5a7409286/), MSc Student in Computer Science at Aarhus University

## Introduction 
Sentiment Analysis is a process of capturing the sentiment of a text, in our case, that sentiment can be **negative**, **neutral**, or **positive**. 

We receive encrypted embeddings, and we need to capture one of the three sentiments, i.e., this is a **secure multiclass classification problem**. The one solution that will be explained here is to train a Logistic Classifier with a multinomial option and then use weights and bias from this training in order to run encrypted inference.  

Usually, for a Logistic Multinomial Classifier, inference would look like the following:

$$y = \text{softmax(Wx+b)}$, $z = \text{arg max}(y)$$

Where:
- $W \in \mathbb{R}^{3 \times 768}$ - weights 
- $b \in R^3$ - bias 
- $y$ - probabilities that the input has a certain sentiment, e.g $[0.05, 0.8, 0.15]$.
- $z$ - actual sentiment $z \in \{0, 1, 2\}$.

The proposed inference we implement is a little bit different, namely, we notice that the decryptor will do the argmax after decryption, so we can just return logits and not compute softmax, which made this solution much faster and easier to implement. So, our goal is to "only" compute $W \cdot x + b$

We make `W_pt` that will be a vector of three ciphertexts representing $W_0$, $W_1$, $W_2$, where $W_i$ are rows of $W$, and `b_pt` representing the vector $b = [b_0, b_1, b_2]$. 
```c++
std::vector<std::vector<double>> W = /* */
std::vector<double> b = /* */ 
int W_len = W.size();
std::vector<Plaintext> W_pt(W_len);

for(int i = 0 ; i < W_len; ++i){
	W_pt[i] = this->m_cc->MakeCKKSPackedPlaintext(W[i]);
}
auto b_pt = this->m_cc->MakeCKKSPackedPlaintext(b);
```

We can divide our computation in three segments: 
1. Inner product 
2. Masking 
3. Summation 

## Inner product
First, we compute the dot product between one encrypted input and plaintext weight vectors. Additionally, we apply OpenMP to parallelize the computation.   
```c++
std::vector<Ciphertext<DCRTPoly>> res(W_len);

#pragma omp parallel for
for (int i = 0; i < W_len; ++i) {
	res[i] = m_cc->EvalInnerProduct(m_InputC, W_pt[i], 768); // 768 -> block size
}
```

`EvalInnerProduct` multiplies $W_i$ with $x$ and sums all the slots in a block into the first slot of that block. In our case, we are only interested in the first slot of the resulting ciphertext.

## Masking
Since the resulting ciphertext will have other values as non zero, we would like to just keep the first value in the ciphertext(this will be important for our next step), so we multiply each of the ciphertext with the suitable mask(the one that has `1.0` in the first slot and `0.0` in the rest). 

```c++
auto slot_count = this->m_cc->GetRingDimension()/2;
std::vector<double> mask = std::vector<double>(slot_count, 0.0);
mask[0] = 1.0;
auto mask_pt = this->m_cc->MakeCKKSPackedPlaintext(mask);

for(int i = 0; i < W_len; ++i){
	res[i] = this->m_cc->EvalMult(res[i], mask_pt);
};
```

## Summation
Now, in order to get $W \cdot x+ b$, we need to put the values of $W_1 \cdot x$ and $W_2 \cdot x$ into the second and third slot and add them up with $b$. We do this by (right)rotating the $W_1 \cdot x$ by `1` and rotating $W_2 \cdot x$ by $2$ and adding them up with $W_0 \cdot x$. Visually, 

![sum2.drawio.png](https://d2lkyury6zu01n.cloudfront.net/images/sentiment_sum.png)

In code: 
```c++
auto rot1 = this->m_cc->EvalRotate(res[1], -1); // -i -> rotate in right by i 
auto rot2 = this->m_cc->EvalRotate(res[2], -2);

auto ctxts = {
	res[0], rot1, rot2
};

this->m_OutputC = this->m_cc->EvalAdd(this->m_cc->EvalAddMany(ctxts), b_pt);
```

## Results
Total multiplicative depth in the end is `2`, `EvalInnerProduct` consumes one level and multiplying by mask consumes another. 

We achieve 73.769% accuracy and 0.166s runtime. 

**Sidenote:** I chose not to pack them into one ciphertext because we would need to do two rotations and one `AddMany` in order to replicate the given input three times. I decided to just parallelize the three inner products, which is fine in this case because we need to do it only three times. 
