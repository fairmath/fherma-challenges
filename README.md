# fherma-challenges

[FHERMA](https://fherma.io/challenges) is a platform dedicated to Fully Homomorphic Encryption (FHE) challenges.

Follow the links provided below to find more details about the platform, participant guides and supported libraries:

- [About FHERMA](https://fherma.io/about) — Information about FHERMA, the challenge committee, and contact details.
- [FHERMA participation guide](https://fherma.io/how_it_works) — Details on FHERMA challenges and requirements.
- [OpenFHE](https://github.com/openfheorg/openfhe-development) — Repository, README, and installation guide.
- [OpenFHE Python](https://github.com/openfheorg/openfhe-python) — Repository, README, and installation guide.
- [OpenFHE-rs](https://crates.io/crates/openfhe) — Rust wrapper, a [walk-through tutorial](https://fherma.io/content/660174e7fce06722c1149a95) and [documentation](https://openfhe-rust-wrapper.readthedocs.io/en/latest/).
- [Apple Swift-Homomorphic-Encryption](https://github.com/apple/swift-homomorphic-encryption) — Repository, README, and installation guide.
- [FHE Resources](https://fhe.org/resources) — A vast collection of resources, including tutorials and walk-throughs, use-cases and demos.
- [Polycircuit](https://github.com/fairmath/polycircuit) — FHE Components Library

# Templates
The `templates` folder contains starter templates for your project. While some challenge folders may also include specific templates, this folder provides the most generic templates, which must be adjusted before submission.

Available templates:
- `openfhe`: template for a C++ OpenFHE-based solution.
- `openfhe-python`: template for an OpenFHE-Python-based solution.

# How to Validate Solution Locally
FHERMA offers two types of challenges: white box and black box. You can learn more by following [FHERMA participation guide](https://fherma.io/how_it_works)

## White Box Challenges

You can validate your solution locally using the [fherma-validator](https://hub.docker.com/r/yashalabinc/fherma-validator) docker image for white box challenges validation. 

## Black Box Challenges

For black box challenges, you can find test cases on the Play tab and validate the results yourself before submission. The evaluation metric may vary by challenge, but usually, the primary metric for black box challenges is accuracy.