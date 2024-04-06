import random

from flask import flash, redirect, render_template
from settings import SHORT_LINK_LENGTH, CHARACTER_SET

from . import app
from .forms import URLMapForm
from .models import URLMap


def get_unique_short_id():
    rand_string = ''.join(random.choice(CHARACTER_SET)
                          for __ in range(SHORT_LINK_LENGTH))
    if URLMap.get(rand_string):
        return get_unique_short_id()
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
        URLMap.save(data_urls)
        return render_template('yacut.html', form=form, short=custom_id)
    return render_template('yacut.html', form=form)


@app.route('/<string:short>')
def redirect_view(short):
    original_url = URLMap.query.filter_by(short=short).first_or_404()
    return redirect(original_url.original)
