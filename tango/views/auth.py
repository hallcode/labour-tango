from flask import Blueprint, current_app, render_template, redirect, url_for
from flask_login import logout_user, login_required

import json

from tango.forms.login import LoginForm


bp = Blueprint('auth', __name__)

@bp.route('/login', methods=["GET"])
def login():
    form = LoginForm()
    return render_template('login.html', form=form)


@bp.route('/login', methods=["POST"])
def authenticate():
    form = LoginForm()

    if not form.validate_on_submit():
        return render_template('login.html', form=form)

    return json.dumps(form.data)


@bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home.home'))