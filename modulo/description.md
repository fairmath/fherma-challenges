> *Complete information regarding the challenge, including detailed requirements, dataset specifications, and evaluation criteria, will be provided at a later stage. Stay tuned!*

# Encrypted Modulo Operation (MOD)

This challenge is part of the fundamental operations series, a collection of exercises designed to explore the core arithmetic operations in the encrypted domain. While addition and multiplication are naturally supported in most FHE schemes, nonlinear operations such as modulo present a significant challenge due to their conditional and piecewise nature.

The objective is implement efficient algorithms computing the modulo operation (`c = a mod b`) homomorphically, where both operands are encrypted. 

The solution will be evaluated on multiple test cases including edge case scenarios. See examples in the table below.

| Test Case Type | a | b | Expected c |
| --- | --- | --- | --- |
| Minimum | 0 | 1 | 0 |
| a < b | 5 | 10 | 5 |
| a = b | 12 | 12 | 0 |
| Small numbers | 7 | 4 | 3 |
| Large numbers | 65536 | 255 | 1 |

## Help

If you have any questions, you can:
- Contact us by email [support@fherma.io](mailto:support@fherma.io)
* Join our [Discord](https://discord.gg/NfhXwyr9M5) server and ask your questions in the [#fherma channel](https://discord.com/channels/1163764915803279360/1167875954392187030). You can also find a team in the [teams channel](https://discord.com/channels/1163764915803279360/1246085439480401930)!
- Use [OpenFHE discourse group](https://openfhe.discourse.group/) for OpenFHE-related questions.

Best of luck to all participants!
