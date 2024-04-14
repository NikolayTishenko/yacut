from flask import jsonify, request

from . import app
from .error_handlers import InvalidAPIUsage
from .models import URLMap


@app.route('/api/id/', methods=['POST'])
def add_short_url():
    data = request.get_json()
    if not data:
        raise InvalidAPIUsage('Отсутствует тело запроса')
    if 'url' not in data:
        raise InvalidAPIUsage('\"url\" является обязательным полем!')
    data_urls = URLMap.save(**data)
    return jsonify(data_urls.url_to_dict()), 201


@app.route('/api/id/<string:short>/', methods=['GET'])
def get_original_url(short):
    original_url = URLMap.get(short)
    if not original_url:
        raise InvalidAPIUsage('Указанный id не найден', 404)
    return jsonify({'url': original_url.original}), 200
