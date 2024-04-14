from flask import flash, redirect, render_template

from . import app
from .error_handlers import ShortLinkGenerationError
from .forms import URLMapForm
from .models import URLMap


@app.route('/', methods=['GET', 'POST'])
def index_view():
    form = URLMapForm()
    if form.validate_on_submit():
        original = form.original_link.data
        custom_id = form.custom_id.data
        try:
            URLMap.save(url=original, custom_id=custom_id)
            return render_template('yacut.html', form=form, short=custom_id)
        except ShortLinkGenerationError:
            flash('Предложенный вариант короткой ссылки уже существует.')
            return render_template('yacut.html', form=form)
    return render_template('yacut.html', form=form)


@app.route('/<string:short>')
def redirect_view(short):
    original_url = URLMap.query.filter_by(short=short).first_or_404()
    return redirect(original_url.original)
