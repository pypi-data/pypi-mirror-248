<!-- Update this link with your own project logo -->
# <img src="https://raw.githubusercontent.com/Cutwell/readme-template/main/logo.svg" style="width:64px;padding-right:20px;margin-bottom:-8px;"> README Template
 A template project / CLI tool for creating a README and other files for Python projects on GitHub.

<!-- Find new badges at https://shields.io/badges -->
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

- This project contains templates you can use to write your own `README`, `CONTRIBUTING` and `PULL_REQUEST_TEMPLATE` files.
- It also includes a CLI tool for using these files in your own projects.
- Supports `pip` or `poetry` for dependency management.

[![Demo of the Read Me template command line app. It shows the user inputting their GitHub username and a repository name to generate a set of customised files useful for sharing GitHub projects.](demo.gif)](https://github.com/faressoft/terminalizer)

## Install

```sh
pip install readme-template-cli
```

## Run locally

### Install dependencies

If using `pip`:

```sh
pip install -r requirements.txt
```

If using `poetry`:

```sh
poetry install --without dev
```

### Usage

Run the program from the command line (from the project root) like this:

If using `pip`:

```sh
python3 readme_generator/src/generator.py
```

If using `poetry`:

```sh
poetry run readme
```

|Flag|Description|
|:---:|:---:|
|`--force`|Force overwrite existing files.|
|`--test`|Run in test mode - files created have .test extension. This does not update filename references inside the templates.|
|`-h`, `--help`|Show this help message and exit.|

## Contributing

<!-- Remember to update the links in the `.github/CONTRIBUTING.md` file from `Cutwell/readme-template` to your own username and repository. -->

For information on how to set up your dev environment and contribute, see [here](.github/CONTRIBUTING.md).

## License

MIT
