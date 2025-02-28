"""Main script for the API documentation web server."""

import os
import re
import urllib.request
from pathlib import Path

import yaml
from flask import Flask, abort, request

app = Flask(__name__)
apis = {}  # API register


@app.route("/")
def index():
    """Generate the index page with a list of APIs."""
    result = []
    for api in apis.values():
        api["favicon"] = api.get("favicon") or config["default-favicon"]
        result.append(
            """<li><img src="{favicon}"> <a href="{path}">{name}</a> &ndash; {description}</li>""".format(**api)
        )
    return index_template.replace("{{api-list}}", "".join(result))


@app.route("/<path>")
def show_api(path: str):
    """Generate the API documentation page for a specific API."""
    if path not in apis:
        abort(404)
    api = apis[path]
    return (
        api_template.replace("{{title}}", api["name"] + " API")
        .replace("{{spec-url}}", api["oas-file"])
        .replace("{{topbar}}", "none")
        .replace("{{favicon}}", api.get("favicon") or config["default-favicon"])
    )


@app.route("/test")
def oas_test():
    """Generate the OAS test page."""
    return api_template.replace("{{title}}", "OAS Test").replace("{{spec-url}}", "").replace("{{topbar}}", "show")


@app.route("/fetch")
def fetch_oas():
    """Fetch OAS from URL and return its content.

    This is used to avoid CORS issues when fetching OAS from a different domain.
    """
    url = request.args.get("url")
    if not url:
        return "URL parameter is required", 400

    try:
        with urllib.request.urlopen(url) as response:
            response_content = response.read().decode("utf-8")
    except urllib.error.HTTPError as e:
        if e.code == 404:
            return "URL not found", 404
        return f"HTTP error occurred: {e.reason}", e.code
    except Exception as e:
        return f"An error occurred: {e!s}", 500

    # Determine the mimetype based on the file extension
    if url.endswith((".yaml", ".yml")):
        mimetype = "application/x-yaml"
    elif url.endswith(".json"):
        mimetype = "application/json"
    else:
        mimetype = "application/octet-stream"

    # Return the fetched content as a file
    response = app.response_class(response=response_content, status=200, mimetype=mimetype)
    response.headers["Content-Disposition"] = f"attachment; filename={os.path.basename(url)}"
    return response


@app.route("/reload", methods=["GET", "POST"])
def read_register():
    """Read the API register from a file or URL and update the global variable."""
    # Clear the current register
    apis.clear()
    if re.match(r"https?:\/\/.*", config["register"]):
        with urllib.request.urlopen(config["register"]) as response:
            register_data = response.read()
    else:
        with Path(config["register"]).open(encoding="utf-8") as infile:
            register_data = infile.read()

    for api in yaml.load(register_data, Loader=yaml.SafeLoader)["apis"]:
        apis[api["path"]] = api

    return "API register updated"


def load_config() -> dict:
    """Load the configuration from a YAML file."""
    config_file = Path("config.yaml")
    if not config_file.is_file():
        print("Using default config. Create config.yaml to customize.")
        config_file = Path("config_default.yaml")

    with config_file.open(encoding="utf-8") as infile:
        return yaml.load(infile, Loader=yaml.FullLoader)


def load_templates(config: dict) -> tuple:
    """Load the HTML templates for the index and API pages."""
    index_template_path = Path(config["index-template"])
    api_template_path = Path(config["api-template"])

    with index_template_path.open(encoding="utf-8") as infile:
        index_template = infile.read()

    with api_template_path.open(encoding="utf-8") as infile:
        api_template = infile.read()

    return index_template, api_template


# Read config
config = load_config()

# Load templates
index_template, api_template = load_templates(config)

# Read the API register
read_register()


if __name__ == "__main__":
    # Run using Flask (use only for development)
    app.run(debug=True, threaded=True, host="0.0.0.0")
