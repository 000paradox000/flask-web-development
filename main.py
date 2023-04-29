from flask import Flask
from flask import request
from flask import jsonify

app = Flask(__name__)

@app.route("/")
def index():
    """Root route, return a hello message."""
    return "Hello world!"

@app.route("/headers")
def get_headers():
    """Get the headers of the request and return them as text lines."""
    headers = request.headers
    accept = headers["Accept"]
    user_agent = headers["User-Agent"]
    separator = "<br>" if "text/html" in accept else "\n"
    end_newline = True if "curl" in user_agent else False
    output = ""

    for name, value in headers.items():
        if output:
            output += separator

        output += f"{name}: {value}"

    if end_newline:
        output += separator

    return output

@app.route("/user/<name>")
def user(name: str):
    """User root route, return a hello message."""
    return f"Hello {name}"

@app.route("/url-map")
def get_url_map():
    """Get url map."""
    return str(app.url_map)

@app.route("/request")
def get_request():
    """Get some request parts."""
    response = {}
    keys = [
        "form",
        "args",
        "values",
        "cookies",
        "files",
        "method",
        "endpoint",
        "scheme",
        "is_secure",
        "host",
        "path",
        "full_path",
        "url",
        "base_url",
        "remote_addr",
    ]
    for key in keys:
        response[key] = getattr(request, key)

    response["headers"] = dict(request.headers)
    response["environ"] = str(request.environ)
    response["query_string"] = request.query_string.decode("utf-8")

    return jsonify(response)

def main():
    """Run the flask application if the main module is invoked directly."""
    print("Running from main")
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True,
    )


if __name__ == "__main__":
    main()
