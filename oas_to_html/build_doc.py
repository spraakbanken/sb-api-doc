
import os
import sys
import configparser
import json
import yaml
import urllib.request
import subprocess

from shutil import copyfile


# Read config
if os.path.exists('config.cfg') is False:
    sys.stderr.write("Please copy config_default.cfg to config.cfg and add your settings!")
    sys.stderr.write("Using default settings for now.")
    configfile = 'config_default.cfg'
else:
    configfile = 'config.cfg'


Config = configparser.ConfigParser()
Config.read(configfile)


def parse_register():
    with open(Config.get("BUILD", "register"), 'r') as stream:
        try:
            json_register = yaml.load(stream)
            return json_register["apis"]

        except yaml.YAMLError as e:
            print(e)


def process_apis(apis):
    """Loop through apis and download their specs."""

    # Check if directories exist
    oas_dir_path = Config.get("BUILD", "oas_dir_path")
    assert os.path.exists(oas_dir_path),\
        "OAS dir path does not exist: %s" % oas_dir_path
    html_dir_path = Config.get("BUILD", "html_dir_path")
    assert os.path.exists(html_dir_path),\
        "HTML dir path does not exist: %s" % html_dir_path
    tmp_dir_path = Config.get("BUILD", "tmp_dir_path")
    assert os.path.exists(tmp_dir_path),\
        "Directory for temporary files does not exist: %s" % tmp_dir_path

    for api in apis:
        download_oas(api, oas_dir_path)
        make_html(api, html_dir_path, tmp_dir_path)

    make_index_page(apis, html_dir_path, tmp_dir_path)


def download_oas(api, oas_dir_path):
    """Download a single OAS file."""
    api_name = api["name"]
    oas_file_url = api["oas-file"]

    filename = make_oas_name(api_name, oas_file_url)
    oas_path = os.path.join(oas_dir_path, filename)

    try:
        urllib.request.urlretrieve(oas_file_url, oas_path)
        api["oas_file_path"] = oas_path
    except OSError:
        raise


def make_html(api, html_dir_path, tmp_dir_path):
    """Generate HTML from OAS file."""
    oas_file_path = api.get("oas_file_path", False)

    tmp_html_path = os.path.join(tmp_dir_path, api["name"] + "_index.html")

    if not os.path.exists(html_dir_path):
        os.mkdir(html_dir_path)

    if oas_file_path:
        html_file_path = os.path.join(html_dir_path, api["path"], "index.html")
        api["html_file"] = html_file_path
    else:
        raise("Cannot build html for %s. No html dir path set." % api["name"])

    # Produce temporary html first to check if everything goes well
    result = subprocess.Popen(["npx", "redoc-cli", "bundle", oas_file_path, "--options.expandResponses=all",
                               "untrustedSpec", "-o", tmp_html_path], stdout=subprocess.PIPE)

    # Do the real thing!
    if result.stderr is None:
        subprocess.Popen(["npx", "redoc-cli", "bundle", oas_file_path, "--options.expandResponses=all",
                          "untrustedSpec", "-o", html_file_path], stdout=subprocess.PIPE)
        print("Built documentation for %s." % api["name"])
    else:
        raise(result.stderr)


def make_index_page(apis, html_dir_path, tmp_dir_path):
    """Fill in API information in index.html and deploy it."""
    html_pieces = []

    for api in apis:

        logo_url = get_logo(api["oas_file_path"])
        if logo_url:
            logo = "<img src='%s' alt='%s-logo'>" % (logo_url, api.get("path"))
        else:
            logo = "<i class='fa fa-user-cog'></i>"

        html_pieces.append("""
        <li>
          <a href="%s">
            %s
            %s
          </a>
          &ndash; %s
        </li>
        """ % (api.get("html_file"), logo, api.get("name"), api.get("description"))
        )

    html_list_items = "\n".join(html_pieces)
    index_file = os.path.join(Config.get("BUILD", "static"), "index.html")

    # Insert generated API list into index.html
    with open(index_file, "r") as f:
        html_contents = f.read()
        html_contents = html_contents.replace("[APILIST]", html_list_items)

    try:
        # Write new html.index to temp path
        new_html_index = os.path.join(tmp_dir_path, "index.html")
        with open(new_html_index, "w") as f:
            f.write(html_contents)
    except:
        raise("Failed to build index.html!")
    else:
        # Deploy index.html and styles.css
        copyfile(new_html_index, os.path.join(html_dir_path, "index.html"))
        styles_css = os.path.join(Config.get("BUILD", "static"), "styles.css")
        copyfile(styles_css, os.path.join(html_dir_path, "styles.css"))
        print("Deployed index.html and styles.css.")


def make_oas_name(api_name, url):
    """Make file name from api_name."""
    prefix = api_name.lower().replace(" ", "_")
    basename = os.path.basename(url)
    return prefix + "_" + basename


def get_logo(oas_file):
    """Parse OAS file and try to get logo."""
    filename, file_extension = os.path.splitext(oas_file)

    if file_extension.lower() == ".json":
        with open(oas_file, "r") as f:
            oas = json.load(f)

    elif file_extension.lower() == ".yaml":
        with open(oas_file, "r") as f:
            oas = yaml.load(f)
    else:
        raise("Unknown OAS file extension: '%s'. Could not retrieve logo." % file_extension)

    logo_info = oas["info"].get("x-logo", False)
    if logo_info:
        return logo_info.get("url", False)


if __name__ == '__main__':
    apis = parse_register()
    process_apis(apis)
