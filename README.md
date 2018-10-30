# sb-api-doc
Guidelines for API documentation


## ReDoc

See [ReDoc page on GitHub](https://github.com/Rebilly/ReDoc) for full reference.

Install ReDoc using npm:

    npm install

Build html from Open API Specification:

    redoc-cli bundle [oasfile.[yaml|json]] [--options.[optionName]]

Serve html from Open API Specification:

    redoc-cli serve [oasfile.[yaml|json]] -w [--options.[optionName]]


## build_doc (python)

Install pipenv if it's not on your system:

    pip3 install --user pipenv

Install dependencies:

    pipenv install

Run script:

    pipenv run python build_doc.py
