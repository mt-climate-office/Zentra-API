# Zentra-API
The `zentra` package provides python bindings to the Zentra Cloud REST API.

## What is Zentra Cloud?

## Installation
The `zentra` package is not yet available on PyPI. Until then, install directly from Github using `pip`:

```bash
pip install git+https://github.com/mt-climate-office/Zentra-API
```

## Usage

### `build` functions

### `parse` functions

### `get` functions

## Testing
This project uses [pytest](https://docs.pytest.org/en/latest/) for testing. To test, run:

```bash
python setup.py test
```

## Setting up project
Dependency and environment management is provided by [conda](https://conda.io/docs/) and is described in the [environment.yml] file. To build the environment, [install conda](https://conda.io/docs/user-guide/install/index.html) and simply run this from your console:

``` bash
conda env create -f environment.yml -p envs/mesonet_db
```

To activate the environment, run:

```bash
source activate envs/mesonet_db

# # Windows
# activate myenv
```

To deactivate:
```bash
source deactivate

# # Windows
# deactivate
```

## Scaffolding

This project has been set up using PyScaffold 3.1. For details and usage
information on PyScaffold see [https://pyscaffold.org/].
