#!/usr/bin/env python3

from flask import Flask, request, make_response, jsonify
import re
import os
import subprocess
import shutil


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


# determine app directory
app_dir = os.path.join(
    os.environ.get(
        "XDG_DATA_HOME",
        os.path.expanduser("~/.local/share")
    ),
    __app_name__)

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
        text = data.get("text", "")
        format = data.get("format", "markdown")
        url = data.get("url", "unknown")

        # remember raw blocks
        raw_blocks = re.findall(
            r'<!-- start raw html -->(.*?)<!-- stop raw html -->',
            text,
            flags=re.DOTALL,
        )
        print(raw_blocks)

        # create directory and save input
        rq_dir = os.path.join(
            app_dir,
            re.sub(r"[:/?*]", "_", url)
        )
        os.makedirs(rq_dir, exist_ok=True)
        orig = os.path.join(rq_dir, "orig.html")
        with open(orig, "w", encoding="utf-8") as f:
            f.write(text)

        # convert
        current = os.path.join(
            rq_dir, "current." + edit_ext.get(format, format)
        )
        if format != "raw":
            subprocess.run([
                pandoc,
                orig,
                "-f", "html+raw_html",
                "-t", format,
                "-o", current
            ], check=True)
        else:
            # no conversion for raw
            shutil.copyfile(orig, current)

        # edit
        mtime_before = os.path.getmtime(current)
        # make sure workspace is open
        subprocess.run([
            code,
            rq_dir
        ], check=True)
        # edit in workspace
        subprocess.run([
            code,
            "-r",
            "-w",
            current
        ], check=True)
        edited = os.path.getmtime(current) != mtime_before

        # convert back
        if edited:
            new = os.path.join(rq_dir, "new.html")
            if format != "raw":
                subprocess.run([
                    pandoc,
                    current,
                    "-f", format,
                    "-t", "html",
                    "-o", new
                ], check=True)
            else:
                # no conversion for raw
                shutil.copyfile(current, new)
            with open(new, "r", encoding="utf-8") as f:
                text = f.read()
    except Exception as exception:
        lineno = exception.__traceback__.tb_lineno
        msg = f"{repr(exception)} at line {lineno}"
        print(msg)
        response = jsonify({"error": msg})
        response.status_code = 500
        return response
    # return
    return text


if __name__ == "__main__":
    app.run(debug=True, port=5000)
