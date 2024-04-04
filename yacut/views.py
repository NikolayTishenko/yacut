import random
import string

from flask import flash, redirect, render_template
from settings import SHORT_LINK_LENGTH

from . import app, db
from .forms import URLMapForm
from .models import URLMap


def get_unique_short_id():
    letters_and_digits = string.ascii_letters + string.digits
    rand_string = ''.join(random.sample(letters_and_digits, SHORT_LINK_LENGTH))
    return rand_string


@app.route('/', methods=['GET', 'POST'])
def index_view():
    form = URLMapForm()
    if form.validate_on_submit():
        custom_id = form.custom_id.data
        if URLMap.query.filter_by(short=custom_id).first():
            flash('Предложенный вариант короткой ссылки уже существует.')
            return render_template('yacut.html', form=form)
        if not custom_id:
            custom_id = get_unique_short_id()
        data_urls = URLMap(
            original=form.original_link.data,
            short=custom_id,
        )
        db.session.add(data_urls)
        db.session.commit()
        return render_template('yacut.html', form=form, short=custom_id)
    return render_template('yacut.html', form=form)


@app.route('/<string:short>')
def redirect_view(short):
    original_url = URLMap.query.filter_by(short=short).first_or_404()
    return redirect(original_url.original)
