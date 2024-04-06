from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, URLField
from wtforms.validators import URL, DataRequired, Length, Optional

from settings import USER_LINK_LENGTH


class URLMapForm(FlaskForm):
    original_link = URLField(
        'Введите длинную ссылку',
        validators=[DataRequired(message='Обязательное поле'),
                    URL(message='Не правильный формат сылки')]
    )
    custom_id = StringField(
        'Введите ваш вариант короткой ссылки',
        validators=[Length(max=USER_LINK_LENGTH,
                           message=('Длина долдна быть не больше '
                                    f'{USER_LINK_LENGTH} символов')),
                    Optional()]
    )
    submit = SubmitField('Создать')
