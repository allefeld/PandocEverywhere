#!/usr/bin/env python3

from flask import Flask, request, make_response, jsonify
import re
import os
import subprocess
import tempfile
from urllib.parse import urlparse


__app_name__ = "PandocEverywhere"
__version__ = "1.1.0"

# non-standard file extensions for Pandoc formats
edit_ext = {
    "markdown": "md",
    "html": "html",
    "html+raw_html": "html",
    "raw": "html"
}

pandoc = "/opt/quarto/bin/tools/pandoc"
code = "/usr/bin/code"
app_dir = os.path.join(tempfile.gettempdir(), __app_name__ + "-" + __version__)

app = Flask(__name__)


# add CORS header to all responses
@app.after_request
def add_cors_headers(response):
    response.headers["Access-Control-Allow-Origin"] = "*"
    return response


# handle preflight request
@app.route("/", methods=["OPTIONS"])
def handle_options():
    response = make_response()
    response.headers["Access-Control-Allow-Methods"] = "POST, OPTIONS"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type"
    return response


# handle actual request
@app.route("/", methods=["POST"])
def handle_post():
    try:
        # process request
        data = request.get_json()
        text = data.get("text")
        format = data.get("format")
        url = data.get("url", "")
        id = data.get("id", "")

        # create name for edited file
        up = urlparse(url)
        fn = re.sub(r'[/:?*]+', '-', up.netloc + up.path + "_" + id)
        fn = os.path.join(app_dir, fn + "." + edit_ext.get(format, format))
        # make sure app_dir exists
        os.makedirs(app_dir, exist_ok=True)

        # patched = re.sub(r'\s+data-mce-[^\s=]+="[^"]*"', "", text)

        # convert text to format
        if format != "raw":
            text_c = convert(text, "html+raw_html", format)
        else:
            # no conversion for "raw"
            text_c = text

        # write converted text to file
        with open(fn, "w") as f:
            f.write(text_c)

        # edit file
        mtime_before = os.path.getmtime(fn)
        subprocess.run([
            code,
            "-n",
            "-w",
            fn
        ], check=True)
        edited = os.path.getmtime(fn) != mtime_before

        if not edited:
            # return original text
            return text

        # read converted & edited text from file
        with open(fn, "r") as f:
            text_ce = f.read()

        # back-convert converted & edited text
        if format != "raw":
            text_ceb = convert(text_ce, format, "html+raw_html")
        else:
            # no conversion for "raw"
            text_ceb = text_ce

        # return back-converted text
        return text_ceb
    except Exception as exception:
        lineno = exception.__traceback__.tb_lineno
        msg = f"{repr(exception)} at line {lineno}"
        print(msg)
        response = jsonify({"error": msg})
        response.status_code = 500
        return response

# use Pandoc to convert between formats, preserving marked HTML as-is
def convert(input, format_from, format_to):
    input = input.replace(
        "<!-- start raw html -->",
        "<script><!-- start raw html -->"
    ).replace(
        "<!-- stop raw html -->",
        "<!-- stop raw html --></script>"
    )
    cp = subprocess.run(
        [pandoc, "-f", format_from, "-t", format_to],
        text=True,
        input=input,
        capture_output=True,
        check=True)
    output = cp.stdout
    output = output.replace(
        "<script><!-- start raw html -->",
        "<!-- start raw html -->"
    ).replace(
        "<!-- stop raw html --></script>",
        "<!-- stop raw html -->"
    )

    return output


if __name__ == "__main__":
    app.run(debug=True, port=5000)
