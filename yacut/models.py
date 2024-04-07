import random
import re
from datetime import datetime

from flask import url_for
from settings import (CHARACTER_SET, SHORT_LINK_LENGTH, SHORT_URL_PATTERN,
                      USER_LINK_LENGTH)

from yacut import db

from .error_handlers import InvalidAPIUsage


class URLMap(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(db.String(), nullable=False)
    short = db.Column(db.String(USER_LINK_LENGTH), unique=True, nullable=False)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def url_to_dict(self):
        return dict(
            url=self.original,
            short_link=url_for('redirect_view',
                               short=self.short,
                               _external=True
                               )
        )

    @staticmethod
    def get_unique_short_id():
        rand_string = ''.join(random.choices(CHARACTER_SET,
                                             k=SHORT_LINK_LENGTH))
        if URLMap.get(rand_string):
            raise InvalidAPIUsage('Кончились варианты коротких ссылок.')
        return rand_string

    @staticmethod
    def save(original, short):
        if short:
            if len(short) > USER_LINK_LENGTH or not re.match(SHORT_URL_PATTERN,
                                                             short):
                raise InvalidAPIUsage('Указано недопустимое имя '
                                      'для короткой ссылки')
            if URLMap.get(short):
                raise InvalidAPIUsage('Предложенный вариант короткой '
                                      'ссылки уже существует.')
        else:
            short = URLMap.get_unique_short_id()
        data_urls = URLMap(
            original=original,
            short=short
        )
        db.session.add(data_urls)
        db.session.commit()
        return data_urls

    @staticmethod
    def get(short):
        return URLMap.query.filter_by(short=short).first()
