import hashlib
from flask import Blueprint, current_app, render_template, request
from tango.models.messages import exclusion_list
from tango import db


bp = Blueprint('email', __name__, url_prefix='/email')


@bp.route('/unsubscribe')
def unsub():
    """Add a user's email address to the exclusion list"""
    email = request.args.get('e')
    if email is None:
        message = 'No email provided.'
        return render_template('unsub.html', message=message)

    hash = hashlib.blake2b()
    hash.update(bytes(email, encoding='utf-8'))
    insert_q = exclusion_list.insert().values(
        hash = hash.hexdigest()
    )

    try:
        result = db.session.execute(insert_q)
        db.session.commit()
    except:
        pass

    message = 'You have been unsubscribed from any emails from Committee Room.'

    return render_template('unsub.html', message=message)