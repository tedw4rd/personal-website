from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def show_home():
    return render_template("index.html")


@app.route("/stylesheets/<path:to_file>")
def send_css(to_file):
    return app.send_static_file("stylesheets/" + to_file)


@app.route("/images/<path:to_file>")
def send_image(to_file):
    return app.send_static_file("images/" + to_file)


@app.route("/javascripts/<path:to_file>")
def send_js(to_file):
    return app.send_static_file("javascripts/" + to_file)