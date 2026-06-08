# API Portal

This Flask application presents a list of the available APIs, and generates HTML versions of the APIs using
[Redoc](https://github.com/Redocly/redoc).

## Requirements

* [Python](https://www.python.org/) 3.12 or newer

## Installation

* Install Python dependencies from `pyproject.toml`.
* Optionally copy `config_default.cfg` to `config.cfg` and make necessary changes.

## Running the application

Host a local web server:

`python apidoc.py`
