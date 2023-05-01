import datetime
from pathlib import Path
import os

import requests
import dotenv
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from flask import Flask
from flask import request
from flask import jsonify
from flask import make_response
from flask import redirect
from flask import url_for
from flask import abort
from flask import render_template


# Load environment variables
dotenv.load_dotenv()

# Paths
base_dir = Path(__file__).resolve().parent
database_path = base_dir / "db" / "fwd.db"

# Database
db = SQLAlchemy()

# Flask application
app = Flask(__name__)

# Database
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{database_path.as_posix()}"
db.init_app(app)

# Database Models
class Role(db.Model):
    __tablename__ = "roles"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True)
    users = db.relationship("User", backref="role")

    def __repr__(self) -> str:
        return self.name

class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, index=True)
    role_id = db.Column(db.Integer, db.ForeignKey("roles.id"))

    def __repr__(self) -> str:
        return self.username


# Create database tables
with app.app_context():
    db.create_all()

migrate = Migrate(app, db)

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

    # latitude = "4.624335"
    # longitude = "-74.063644"
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

@app.route("/error-400")
def get_error_400():
    """Example of status code 400 BAD REQUEST."""
    return "<h1>Error 400</h1>", 400

@app.route("/cookies")
def get_or_create_cookie():
    """Example of creating or getting a cookie."""
    key = "internet"
    value = "casi complejo"
    response = make_response(f"Cookie created, key={key}, value={value}")
    response.set_cookie(key, value)

    return "<h1>No Error</h1>", 200

@app.route("/redirect")
def make_redirect():
    """Make a redirection."""
    return redirect(url_for("receive_redirect"))

@app.route("/receive-redirect")
def receive_redirect():
    """Response of redirection."""
    return "Redirect received", 200

@app.route("/abort")
def abort_execution():
    """Example of aborting executions."""
    print("Before abort")
    abort(404)
    print("After abort")
    return "Execution not aborted", 200

@app.route("/profile")
def profile():
    """Display profile in a template."""
    template_name_or_list = "profile/profile.html"
    context = {
        "name": "Miguel de Icaza"
    }
    return render_template(
        template_name_or_list,
        **context
    )

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
