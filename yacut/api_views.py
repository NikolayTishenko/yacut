import re

from flask import jsonify, request
from settings import SHORT_URL_PATTERN, USER_LINK_LENGTH

from . import app, db
from .error_handlers import InvalidAPIUsage
from .models import URLMap
from .views import get_unique_short_id


@app.route('/api/id/', methods=['POST'])
def add_short_url():
    data = request.get_json()
    if not data:
        raise InvalidAPIUsage('Отсутствует тело запроса')
    original = data.get('url')
    if not original:
        raise InvalidAPIUsage('\"url\" является обязательным полем!')
    short = data.get('custom_id')
    if short:
        if len(short) > USER_LINK_LENGTH or not re.match(SHORT_URL_PATTERN,
                                                         short):
            raise InvalidAPIUsage('Указано недопустимое имя '
                                  'для короткой ссылки')
        if URLMap.query.filter_by(short=short).first():
            raise InvalidAPIUsage('Предложенный вариант короткой '
                                  'ссылки уже существует.')
    else:
        short = get_unique_short_id()
    data_urls = URLMap(
        original=original,
        short=short
    )
    db.session.add(data_urls)
    db.session.commit()
    return jsonify(data_urls.url_to_dict()), 201


@app.route('/api/id/<string:short>/', methods=['GET'])
def get_original_url(short):
    original_url = URLMap.query.filter_by(short=short).first()
    if not original_url:
        raise InvalidAPIUsage('Указанный id не найден', 404)
    return jsonify({'url': original_url.original}), 200
