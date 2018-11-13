# API Portal

This Flask application presents a list of the available APIs, and generates HTML versions of the APIs using
[ReDoc](https://github.com/Rebilly/ReDoc).

## Requirements

* [Python](https://www.python.org/) 3.4 or newer
* [Pipenv](https://pipenv.readthedocs.io/en/latest/) (install with `pip3 install --user pipenv`)


## Installation

* Install Python dependencies:

    `pipenv install`

* Optionally copy `config_default.cfg` to `config.cfg` and make necessary changes.

## Running the application

`pipenv run gunicorn apidoc:app`
