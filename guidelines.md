# API documentation guidelines

## Open API specification

Documentation of Språkbanken’s REST APIs is done with Open API Specification (OAS). This format is widely used and supported by a large amount of organisations. It can be used for describing, producing, consuming, and visualizing RESTful web services.

The OAS format is described here:
* https://github.com/OAI/OpenAPI-Specification/blob/master/versions/3.0.2.md

Or somewhat more human-readable:
* https://swagger.io/specification/
* https://swagger.io/docs/specification/about/

## Språkbanken's requirements

* The OAS file should be written in YAML or JSON. (There are tools which can convert between these formats.)
* The OAS file must be a valid version 3 OpenAPI Specification.
* The OAS file should “live” together with your code, i.e. it should be stored in the application’s GitHub repository.
* It is up to you whether the specification is programmatically generated (e.g. from docstrings) or written entirely by hand.
* If you would like to include example calls in the description fields, please use the following format (this is not part of the official OpenAPI Specification but rather a Språkbanken addition):

    YAML example:
    ```YAML
    description: |
        Pings the backend, responds with the status of the catapult.

        ### Example

        [`/ping`](https://ws.spraakbanken.gu.se/ws/sparv/v2/ping)
    ```

    JSON example:
    ```JSON
    {
      "description": "Pings the backend, responds with the status of the catapult.\n\n### Example\n\n[`/ping`](https://ws.spraakbanken.gu.se/ws/sparv/v2/ping)\n"
    }

    ```

## Examples

For inspiration, see some of the already available specifications for Språkbanken’s tools:

* Korp
    * [OAS file in YAML](https://raw.githubusercontent.com/spraakbanken/korp-backend/master/docs/api.yaml)
    * [documentation HTML](http://demo.spraakdata.gu.se/apidoc/korp/)

* Sparv
    * [OAS file in JSON](https://raw.githubusercontent.com/spraakbanken/sparv-backend/oas-adapt/app/static/sparv_api_spec.json)
    * [documentation HTML](http://demo.spraakdata.gu.se/apidoc/sparv/)

## Template

Check the template files [`template.yaml`](templates/template.yaml) and [`template.json`](templates/template.json) for a basic skeleton of an OAS.

## Tools

### Tools for writing/generating OAS

* [Swagger-editor](http://editor.swagger.io): Writing OAS with instant evaluation and generation of interactive documentation
* [ReadMe oas](https://openap.is/): Generate OAS from inline-code annotations
* [Openapi-spec-validator](https://github.com/p1c2u/openapi-spec-validator): Python library for validating OAS files
* [Swagger Inspector](https://swagger.io/tools/swagger-inspector/): Online tool for generating OAS files from example calls. (Requires user account.)

### Generating code from API specifications

* [OpenAPI Generator](https://openapi-generator.tech/): Allows generation of API client libraries (SDK generation), server stubs, documentation and configuration automatically given an OpenAPI Spec.
