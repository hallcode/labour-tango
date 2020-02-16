"""
Login functions and handlers.
"""
from tango import login_manager
from tango.models.user import User

@login_manager.user_loader
def load_user(user_id):
    user = User.query.get(user_id)
    return user