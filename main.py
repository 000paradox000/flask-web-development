import datetime
import os

import requests
import dotenv

from flask import Flask
from flask import request
from flask import jsonify

dotenv.load_dotenv()
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
    response["query_string"] = request.query_string.decode("utf-8")

    return jsonify(response)


@app.route("/temperature")
def get_temperature():
    """Get the temperature of Bogotá."""
    now = datetime.datetime.now()
    day_name = now.strftime("%A")
    month_name = now.strftime("%B")
    date_string = now.strftime("%Y-%m-%d")
    time_string = now.strftime("%H:%M:%S")
    temperature = ""

    latitude = "4.624335"
    longitude = "-74.063644"
    base_url = "https://api.openweathermap.org/data/2.5/weather"
    api_key = os.environ["OPENWEATHER_API_KEY"]
    query_string = f"appid={api_key}&q=bogota&units=metric"
    url = f"{base_url}?{query_string}"
    temperature = requests.get(url).json()["main"]["temp"]

    response = {
        "city": "Bogotá",
        "date": date_string,
        "time": time_string,
        "month": month_name,
        "day": day_name,
        "temperature": temperature,
    }

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
