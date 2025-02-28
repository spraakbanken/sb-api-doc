
from collections import OrderedDict
from flask import Flask, abort, request
import os
import yaml
import urllib.request
import re

app = Flask(__name__)


@app.route("/")
def index():
    result = []
    for api in apis.values():
        api["favicon"] = api.get("favicon") or config["default-favicon"]
        result.append("""<li><img src="{favicon}"> <a href="{path}">{name}</a> &ndash; {description}</li>""".format(**api))
    return index_template.replace("{{api-list}}", "".join(result))


@app.route("/<path>")
def show_api(path):
    if not path in apis:
        abort(404)
    api = apis[path]
    html = api_template.replace("{{title}}", api["name"] + " API").replace("{{spec-url}}", api["oas-file"]).replace(
        "{{topbar}}", "none").replace("{{favicon}}", api.get("favicon") or config["default-favicon"])
    return html


@app.route("/test")
def oas_test():
    html = api_template.replace("{{title}}", "OAS Test").replace("{{spec-url}}", "").replace("{{topbar}}", "show")
    return html


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
        return f"An error occurred: {str(e)}", 500

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
    global apis
    apis = OrderedDict([])

    if re.match(r"https?:\/\/.*", config["register"]):
        with urllib.request.urlopen(config["register"]) as response:
            register_data = response.read()
    else:
        with open(config["register"]) as infile:
            register_data = infile.read()

    for api in ordered_load(register_data)["apis"]:
        apis[api["path"]] = api

    return "API register updated"


def ordered_load(stream, Loader=yaml.Loader, object_pairs_hook=OrderedDict):
    """Preserve order in yaml.load(). Needed for Python < 3.6."""
    class OrderedLoader(Loader):
        pass

    def construct_mapping(loader, node):
        loader.flatten_mapping(node)
        return object_pairs_hook(loader.construct_pairs(node))

    OrderedLoader.add_constructor(
        yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG,
        construct_mapping)
    return yaml.load(stream, OrderedLoader)


# Read config
if os.path.isfile("config.yaml"):
    config_file = "config.yaml"
else:
    print("Using default config. Create config.yaml to customize.")
    config_file = "config_default.yaml"

with open(config_file) as infile:
    config = yaml.load(infile, Loader=yaml.FullLoader)

# Load templates
with open(config["index-template"]) as infile:
    index_template = infile.read()

with open(config["api-template"]) as infile:
    api_template = infile.read()

read_register()


if __name__ == "__main__":
    # Run using Flask (use only for development)
    app.run(debug=True, threaded=True, host="0.0.0.0")
