from flask import Flask, render_template, abort
from flask.ext.sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")
app.config['CSRF_ENABLED'] = False
app.secret_key = os.environ.get("SECRET_KEY")

db = SQLAlchemy(app)

from models import *

db.create_all()

from flask.ext.admin import Admin
from flask.ext.admin.contrib.sqlamodel import ModelView

admin = Admin(app)

admin.add_view(ModelView(LinkCategory, db.session))
admin.add_view(ModelView(Link, db.session))

@app.route("/")
def show_home():
    cat_query = LinkCategory.query.order_by(LinkCategory.rank)
    all_cats = []
    for cat in cat_query:
        all_cats.append({"text": cat.name, "url":"/" + cat.stub, "description":""})
    return render_template("blocks.html", links=all_cats, trail=[])


@app.route("/about")
def show_about():
    return render_template("about.html", links=[], trail=[{"link": "/about", "text":"ABOUT", "current":True}])


@app.route("/<stub>/all")
def show_category(stub):
    cat = LinkCategory.query.filter_by(stub=stub).first()
    if cat is None:
        abort(404)
    links = Link.query.filter_by(category_id=cat.id).order_by(Link.rank)
    display_links = []
    for l in links:
        display_links.append({"text":l.display_text, "url":l.url, "description":l.description})

    return render_template("blocks.html", links=display_links, trail=[{"link": stub, "text":cat.name, "current":False},{"link": stub, "text":"ALL", "current":True}])


@app.route("/<stub>")
def show_category(stub):
    cat = LinkCategory.query.filter_by(stub=stub).first()
    if cat is None:
        abort(404)
    links = Link.query.filter_by(category_id=cat.id).order_by(Link.rank)
    display_links = []
    for l in links[:5]:
        display_links.append({"text":l.display_text, "url":l.url, "description":l.description})

    if len(links.all()) > 5:
        display_links.append({"text":"ALL", "url":"/%s/%s" % (stub, "all"), "description": ""})

    return render_template("blocks.html", links=display_links, trail=[{"link": stub, "text":cat.name, "current":True}])


@app.route("/stylesheets/<path:to_file>")
def send_css(to_file):
    return app.send_static_file("stylesheets/" + to_file)


@app.route("/images/<path:to_file>")
def send_image(to_file):
    return app.send_static_file("images/" + to_file)


@app.route("/javascripts/<path:to_file>")
def send_js(to_file):
    return app.send_static_file("javascripts/" + to_file)