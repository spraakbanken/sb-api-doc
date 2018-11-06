# API Documentation at Språkbanken

The goal of this project is to standardise the documentation of REST APIs
at Språkbanken.

This repository contains:

* guidelines for API documentation
* a register for Open API Specification files
* code for generating html documentation from Open API Specification files


## API Documentation Guidelines

Please check the [guidelines document](guidelines.md) for more information on how to write documentation for Språkbanken's
REST APIs.


## Automatic Generation of HTML Documentation

By registering your Open API Specification (OAS) file in [`oas-register.yaml`](oas-register.yaml) an HTML version of the
documentation will be generated automatically and published to the [SB API documentation portal](http://demo.spraakdata.gu.se/apidoc).

To register your API documentation please add the following information to [`oas-register.yaml`](oas-register.yaml):
  * `name`: The name of your API (used as meta data only).
  * `oas-file`: The URL from where the OAS file can be retrieved. This URL must be accessible from Språkbanken's servers.
  * `path`: The path to your API documentation that will be created automatically. This path should be relative to the
    [SB API documentation portal](http://demo.spraakdata.gu.se/apidoc). E.g. if the `path` is set to `sparv` the documentation
    will be available at http://demo.spraakdata.gu.se/apidoc/sparv.
  * `description`: A very short description of the API.

* *TODO: What happens after filling in the oas-register? nightly build of HTML*
* *TODO: Redoc test page (paste a URL or document and get a preview of the Redoc HTML)*
