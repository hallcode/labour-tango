"""
Login functions and handlers.
"""
from flask import flash, redirect, url_for, request
from tango import login_manager
from tango.models.user import User

@login_manager.user_loader
def load_user(user_id):
    user = User.query.get(user_id)
    return user


@login_manager.unauthorized_handler
def handle_needs_login():
    flash("You must be logged in to access this page.", "error")
    return redirect(url_for('auth.login', next=request.endpoint))