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
documentation will automatically be available on the [SB API documentation portal](https://ws.spraakbanken.gu.se/docs/).

To register your API documentation please add the following information to [`oas-register.yaml`](oas-register.yaml):
  * `name`: The name of your API (used as meta data only).
  * `oas-file`: The URL from where the OAS file can be retrieved. This URL must be accessible from Språkbanken's servers.
  * `path`: The path to your API documentation that will be created automatically. This path should be relative to the
    [SB API documentation portal](https://ws.spraakbanken.gu.se/docs/). E.g. if the `path` is set to `sparv` the documentation
    will be available at https://ws.spraakbanken.gu.se/docs/sparv.
  * `description`: A very short description of the API.
  * `favicon`: Optional. A link to the API's favicon.

To preview your API documentation, you can use
the test page available at https://ws.spraakbanken.gu.se/docs/test.


## TODO

* Indexing and search function for all documentations on portal
