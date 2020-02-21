from flask import Blueprint, current_app, render_template


bp = Blueprint('home', __name__)


@bp.route('/')
def home():
    """Serve a home page, depending on if user is logged in."""

    return render_template('home.html', name="World")


@bp.route('/page/<title>')
def page(title):
    return render_template('pages/%s.html' % title.lower())