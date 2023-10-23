from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

subscribe = []

@app.route("/")
def index():
    title = "John's Blog"
    return render_template("index.html", title = title)

@app.route("/about")
def about():
    title = "About"
    names = ["John", "Mary", "Wes", "Sally"]
    return render_template("about.html", names = names, title = title)