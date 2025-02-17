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
## White Box Challenges

You can validate your solution locally using the [fherma-validator](https://hub.docker.com/r/yashalabinc/fherma-validator) docker image for white box challenges validation. To pull the image, run the following comand:

```bash
docker pull yashalabinc/fherma-validator
```
### Example Setup
If your local folder containing the solution is located at `~/user/tmp/fherma-challenge/app`, use the following command to run the validator:

```bash
docker run -ti -v ~/user/tmp/fherma-challenge:/fherma yashalabinc/fherma-validator --project-folder=/fherma/app --testcase=/fherma/tests/test_case.json
```
Here is a breakdown of the command:
- `-v ~/user/tmp/fherma-challenge:/fherma`: maps your local directory to the /fherma directory in the Docker container.
- `--project-folder=/fherma/app`: specifies the folder where your solution is located.
- `--testcase=/fherma/tests/test_case.json`: points to the JSON file containing the test case for validation. Ensure `test_case.json` is added to your directory and the correct path is used in the command. Test cases can be found in the corresponding challenge folders.

After validation, a `result.json` file will be generated in your project folder.
