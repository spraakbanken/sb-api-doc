# sb-api-doc
Guidelines for API documentation


## ReDoc

See [ReDoc page on GitHub](https://github.com/Rebilly/ReDoc) for full reference.

Install ReDoc using npm:

    npm install redoc --save

Or using yarn:

    yarn add redoc

Build html from Open API Specification:

    redoc-cli bundle [oasfile.[yaml|json]] [--options.[optionName]=[value]]

Serve html from Open API Specification:

    redoc-cli serve [oasfile.[yaml|json]] -w [--options.[optionName]=[value]]
