import requests

from flask import redirect, url_for, request, render_template

from tango import login_manager, db
from tango.models.person import Person
from tango.models.user import User
from tango.models.boundary import Boundary
from tango.forms.register import StartForm


def start_handler():
    form = StartForm()

    error = False

    if not form.validate_on_submit():
        error = True

    pc_data = get_postcode_data(form.post_code.data)
    if not pc_data:
        error = True
        form.post_code.errors += ['The postcode you entered was invalid.']

    if error:
        return render_template('register/start.html', form=form)

    person = Person(
        fname=form.first_name.data,
        lname=form.last_name.data,
        email=form.email.data,
        post_code=form.post_code.data,
        mobile_tel=form.tel_no.data
    )

    db.session.add(person)

    constituency_id = pc_data["parliamentary_constituency"]
    constituency = Boundary.query.get(constituency_id)
    if constituency is not None:
        person.boundaries.append(constituency)

    ward_id = pc_data["admin_ward"]
    ward = Boundary.query.get(ward_id)
    if ward is not None:
        person.boundaries.append(ward)


def get_postcode_data(post_code):
    req = requests.get('https://api.postcodes.io/postcodes/%s' % post_code)

    if req.status_code != 200:
        return False

    data = req.json()

    return data["result"]["codes"]