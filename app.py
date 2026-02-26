import json
from flask import Flask, abort, jsonify, request
from flask_restx import Api  # type: ignore

PAGE_SIZE = 25

app = Flask(__name__)
api = Api(app)

with open('awards.json', encoding='utf-8') as f:
    awards = json.load(f)

# TODO: Добавить код для чтения лауреатов из файла


@app.route("/api/v1/awards/")
def awards_list():
    try:
        p = int(request.args.get('p', 0))
        if p < 0:
            raise ValueError
    except ValueError:
        return abort(400)
    page = awards[p * 50:(p + 1)*50]
    return jsonify({
        'page': p,
        'count_on_page': PAGE_SIZE,
        'total': len(awards),
        'items': page,
    })


@app.route("/api/v1/award/<int:pk>/")
def award_object(pk):
    if 0 <= pk < len(awards):
        return jsonify(awards[pk])
    else:
        abort(404)


# TODO: Добавить код для получения списка лауреатов


# TODO: Добавить код для получения лауреата по индексу
