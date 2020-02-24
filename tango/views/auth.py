from flask import Blueprint, render_template, redirect, url_for, flash, request, session
from flask_login import logout_user, login_required, login_user, current_user

from tango.models.user import User

from tango.forms.login import LoginForm
from tango.forms.register import PAGES
from tango.services.register import your_details_handler, preferences_handler, account_handler


bp = Blueprint('auth', __name__)


@bp.route('/login', methods=["GET"])
def login():
    form = LoginForm()
    return render_template('login.html', form=form)


@bp.route('/login', methods=["POST"])
def authenticate():
    form = LoginForm()

    message = """Email or password was not recognised. 
                 Please try again or <a href="%s">create an account</a>.""" \
              % url_for('auth.register')

    if not form.validate_on_submit():
        return render_template('login.html', form=form)

    user = User.query.filter_by(email=form.email.data).first()

    if user is None:
        flash(message, 'error')
        return redirect(url_for('auth.login'))

    if not user.check_password(form.password.data):
        flash(message, 'error')
        return redirect(url_for('auth.login'))

    login_user(user, remember=form.remember_me.data)

    next = request.args.get('next')
    try:
        dest_url = url_for(next)
    except:
        dest_url = url_for('home.home')

    return redirect(dest_url)


@bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home.home'))


@bp.route('/volunteer', defaults={'page':'Start'}, methods=["GET","POST"])
@bp.route('/volunteer/<page>', methods=["GET","POST"])
def register(page):
    if current_user.is_authenticated:
        flash("You already have an account.", "error")
        return redirect(url_for('home.home'))

    if request.method == "GET":
        form=None
        if page != "Start" and page != 'Done':
            if "registration_started" not in session.keys():
                return redirect(url_for('auth.register', page='Start'))

            if page != 'YourDetails' and "person_id" not in session.keys():
                return redirect(url_for('auth.register', page='YourDetails'))

            form_page = PAGES[page]
            form = form_page()

        if page == "Start":
            session["registration_started"] = True

        return render_template('register/%s.html' % page.lower(), form=form)

    if request.method == "POST":
        if page == "YourDetails":
            return your_details_handler()
        if page == "Preferences":
            return preferences_handler()
        if page == 'Account':
            return account_handler()
