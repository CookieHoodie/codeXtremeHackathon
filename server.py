
from flask import render_template
from flask import jsonify
from flask import request
from flask import Flask

from visualize.datahub import BingData

app = Flask(__name__)


@app.route('/')
def index():
    return render_template("visualize.html")


@app.route('/data')
def data():
    searched_text = request.args.get("q")
    if not searched_text:
        return jsonify("nothing is searched")

    search_engine = BingData("a17baead8c094adeaddb46a215432441")
    search_engine.search_for(searched_text)
    return jsonify(search_engine.get_tokenized_titles())


# @app.route('/data')
# def data():
#     searched_text = request.args.get("q")
#     if not searched_text:
#         return jsonify({"title": "NOTHING IS SEARCED"})
#
#     search_engine = BingData("71ae7eafb04c4edda1f4a8edc21fb7dc")
#     search_engine.search_for(searched_text)
#
#     return jsonify({"title": search_engine.get_tokenized_titles(), "webpages": search_engine.get_joined_webpages_list()})

