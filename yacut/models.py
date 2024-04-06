from datetime import datetime

from flask import url_for
from settings import USER_LINK_LENGTH

from yacut import db


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

    def save(data_urls):
        db.session.add(data_urls)
        db.session.commit()

    def get(short):
        return URLMap.query.filter_by(short=short).first()
