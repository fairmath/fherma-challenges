> *Complete information regarding the challenge, including detailed requirements, dataset specifications, and evaluation criteria, will be provided at a later stage. Stay tuned!*

# Private Feature Engineering Pipeline

Feature engineering is a critical step in any machine learning pipeline, shaping raw data into forms suitable for model training and analysis. In this challenge, participants are tasked with performing key feature-engineering operations: normalization, standardization, and statistical summarization entirely on encrypted dataset.

The goal is to design a pipeline that maintains data privacy while accurately transforming and summarizing the data without ever decrypting intermediate values.

## Pipeline Components

### Statistics

#### Quantiles

Given a dataset $x_1, ..., x_n$, the **α-quantile** is the value q such that:

$$
P(X \le q) = \alpha
$$

- Minimum: $\alpha = 0.00$
- 1st quartile (Q1): $\alpha = 0.25$
- Median (Q2): $\alpha = 0.50$
- 3rd quartile (Q3): $\alpha = 0.75$
- Maximum: $\alpha = 1.00$

#### Mean & Variance

- Mean of a dataset $x_1, ..., x_n$:

$$
\mu = \frac{1}{n} \sum_{i=1}^{n} x_i 
$$

- Variance of a dataset $x_1, ..., x_n$:

$$
\sigma = \sqrt{\sigma^2}
$$

## Transformation

### Min–Max Normalization

$$
x' = \frac{x - \min(x)}{\max(x) - \min(x)}
$$

### Standardization

$$
x' = \frac{x - \mu}{\sigma}
$$

## Help

If you have any questions, you can:
- Contact us by email [support@fherma.io](mailto:support@fherma.io)
* Join our [Discord](https://discord.gg/NfhXwyr9M5) server and ask your questions in the [#fherma channel](https://discord.com/channels/1163764915803279360/1167875954392187030). You can also find a team in the [teams channel](https://discord.com/channels/1163764915803279360/1246085439480401930)!
- Use [OpenFHE discourse group](https://openfhe.discourse.group/) for OpenFHE-related questions.

Best of luck to all participants!
