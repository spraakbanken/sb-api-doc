
import os
import configparser
import yaml
import urllib.request
import subprocess

# Read config
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

    # Get path for npx executable
    get_npx_path = subprocess.Popen(["which", "npx"], stdout=subprocess.PIPE)
    npx_path, _stderr = get_npx_path.communicate()
    npx_path = npx_path.decode().rstrip("\n")

    # Produce temporary html first to check if everything goes well
    result = subprocess.Popen([npx_path, "redoc-cli", "bundle", oas_file_path, "--options.expandResponses=all",
                               "untrustedSpec", "-o", tmp_html_path], stdout=subprocess.PIPE)

    # Do the real thing!
    if result.stderr is None:
        subprocess.Popen([npx_path, "redoc-cli", "bundle", oas_file_path, "--options.expandResponses=all",
                          "untrustedSpec", "-o", html_file_path], stdout=subprocess.PIPE)
        print("Built documentation for %s." % api["name"])
    else:
        raise(result.stderr)


def make_oas_name(api_name, url):
    """Make file name from api_name."""
    prefix = api_name.lower().replace(" ", "_")
    basename = os.path.basename(url)
    return prefix + "_" + basename


if __name__ == '__main__':
    apis = parse_register()
    process_apis(apis)
