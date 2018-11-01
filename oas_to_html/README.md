# Generation of HTML Documentation with Python and Redoc

For now Språkbanken uses [Redoc](https://github.com/Rebilly/ReDoc) for conversion of the OAS files into an HTML documentation page.

## Requirements

* [Python](https://www.python.org/) 3.4 or newer
* [pipenv](https://pipenv.readthedocs.io/en/latest/) (install with `pip3 install --user pipenv`)
* [npm](https://www.npmjs.com/)


## Installation

Install python dependencies:

    pipenv install

Install [ReDoc](https://github.com/Rebilly/ReDoc) using npm:

    npm install


## Usage

### build_doc

This python script will parse the yaml register `oas-register.yaml` and download the OAS files for Språkbanken's REST APIs. It will then call ReDoc and build html documentation.

Run `build_doc.py` with pipenv:

    pipenv run python build_doc.py


### ReDoc

ReDoc is used to convert OAS files into HTML. It is called automatically by `build_doc.py` but can also be run separately. See [ReDoc](https://github.com/Rebilly/ReDoc) for full reference.

Build html from Open API Specification:

    npx redoc-cli bundle [oasfile.[yaml|json]] [--options.[optionName]]

Serve html from Open API Specification:

    npx redoc-cli serve [oasfile.[yaml|json]] -w [--options.[optionName]]