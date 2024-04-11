import random
import re
from datetime import datetime

from flask import url_for
from settings import (CHARACTER_SET, SHORT_LINK_LENGTH, SHORT_URL_PATTERN,
                      USER_LINK_LENGTH)

from yacut import db

from .error_handlers import InvalidAPIUsage, ShortLinkGenerationError


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

    def from_dict(self, data):
        for field in ['original', 'short']:
            if field in data:
                setattr(self, field, data[field])

    @staticmethod
    def get_unique_short_id():
        rand_string = ''.join(random.choices(CHARACTER_SET,
                                             k=SHORT_LINK_LENGTH))
        if URLMap.get(rand_string):
            raise ShortLinkGenerationError(
                'Кончились варианты коротких ссылок.')
        return rand_string

    @classmethod
    def save(cls, **data):
        short = data.get('custom_id')
        if short:
            if not re.match(SHORT_URL_PATTERN, short):
                raise InvalidAPIUsage('Указано недопустимое имя '
                                      'для короткой ссылки')
            if cls.get(short):
                raise InvalidAPIUsage('Предложенный вариант короткой '
                                      'ссылки уже существует.')
        else:
            short = cls.get_unique_short_id()
        data_urls = cls(
            original=data.get('url'),
            short=short)
        db.session.add(data_urls)
        db.session.commit()
        return data_urls

    @staticmethod
    def get(short):
        return URLMap.query.filter_by(short=short).first()
