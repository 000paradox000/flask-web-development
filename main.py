from flask import Flask
from flask import request

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
