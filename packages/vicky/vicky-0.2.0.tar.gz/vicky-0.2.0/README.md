# Vicky CLI

Command-line interface for Vicky.

[![Version](https://img.shields.io/pypi/v/vicky.svg?style=flat)](https://pypi.python.org/pypi/vicky/)
[![Build Status](https://github.com/vicktornl/vicky-cli/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/vicktornl/vicky-cli/actions/workflows/ci.yml)

## Compatibility

* Python v3.x

## Features

```
Usage: vicky [OPTIONS] COMMAND [ARGS]...

Options:
  --help  Show this message and exit.

Commands:
  deploy  Deploy a theme to a Vicky instance.
```

## Installation

Install `vicky` with `pip:

```
$ pip install vicky
```

## Usage

Deploy a theme to a Vicky instance:

```
Usage: vicky deploy [OPTIONS] THEME DIRECTORY

  Deploy a theme to a Vicky instance.

Options:
  --custom_css TEXT  path to the file containing custom CSS.
  --custom_js TEXT   path to the file containing custom JavaScript.
  --api-key TEXT     API key of a Vicky instance.
  --version TEXT     version to be set after a successful deployment of a
                     theme.
```

If you don't provide a API key and/or version this will be automatically populated:

* `api_key` - Reads the `VICKY_API_KEY` environment variable
* `version` - The git short hash (`git rev-parse --short HEAD`) of the directory

## Environment variables

* `VICKY_API_KEY` - The API key of your Vicky instance.
* `VICKY_BASE_URL` - The base url of your Vicky instance, e.g. https://instance.vicky-cms.nl
