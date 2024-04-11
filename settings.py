import os
import string


class Config(object):
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI',
                                        default='sqlite:///db.sqlite3')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv('SECRET_KEY')


USER_LINK_LENGTH = 16
SHORT_LINK_LENGTH = 6
CHARACTER_SET = string.ascii_letters + string.digits
SHORT_URL_PATTERN = '^[A-Za-z0-9]{{1,{}}}$'.format(USER_LINK_LENGTH)
