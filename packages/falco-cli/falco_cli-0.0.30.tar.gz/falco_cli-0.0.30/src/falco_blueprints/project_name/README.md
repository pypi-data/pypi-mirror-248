# {{ project_name }}

[![falco](https://img.shields.io/badge/built%20with-falco-success)](https://github.com/Tobi-De/falco)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![linting: pylint](https://img.shields.io/badge/linting-pylint-yellowgreen)](https://github.com/PyCQA/pylint)
[![Hatch project](https://img.shields.io/badge/%F0%9F%A5%9A-Hatch-4051b5.svg)](https://github.com/pypa/hatch)

## Prerequisites

- `Python 3.11+`
- `hatch 1.8.0+`
- `Postgresql 10+`

## Development

### Create a new virtual environment

```shell
hatch shell
```

### Install pre-commit

```shell
pre-commit install
```

### Create a `.env` file

```shell
falco sync-dotenv
```

### Run the django development server

```shell
hatch run server
```
