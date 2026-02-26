import json
from flask import Flask, abort, jsonify, request
from flask_restx import Api  # type: ignore

PAGE_SIZE = 25

app = Flask(__name__)
api = Api(app)

with open('awards.json', encoding='utf-8') as f:
    awards = json.load(f)

with open('laureats.json', encoding='utf-8') as f:
    laureats_data = json.load(f)
    laureats = laureats_data.get('laureates', laureats_data) \
        if isinstance(laureats_data, dict) else laureats_data


@app.route("/api/v1/awards/")
def awards_list():
    try:
        p = int(request.args.get('p', 0))
        if p < 0:
            raise ValueError
    except ValueError:
        return abort(400)
    page = awards[p * PAGE_SIZE:(p + 1) * PAGE_SIZE]
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


@app.route("/api/v2/laureats/")
def laureats_list():
    try:
        p = int(request.args.get('p', 0))
        if p < 0:
            raise ValueError
    except ValueError:
        return abort(400)
    page = laureats[p * PAGE_SIZE:(p + 1) * PAGE_SIZE]
    return jsonify({
        'page': p,
        'count_on_page': PAGE_SIZE,
        'total': len(laureats),
        'items': page,
    })


@app.route("/api/v2/laureat/<id>/")
def laureat_object(id):
    for laureat in laureats:
        # Безопасное получение 'id' через .get() и приведение к строке
        if str(laureat.get('id')) == str(id):
            return jsonify(laureat)  # Добавлен jsonify
    abort(404)


if __name__ == '__main__':
    app.run(debug=True)
