import requests

from flask import redirect, url_for, request, render_template, session

from tango import login_manager, db
from tango.constants import EMAIL_CONSENT_KEYS, CONSENT_ORIGINS
from tango.models.person import Person, Consent
from tango.models.user import User
from tango.models.boundary import Boundary
from tango.forms.register import StartForm, PreferencesForm, AccountForm


def your_details_handler():
    form = StartForm()

    error = False

    if not form.validate_on_submit():
        error = True

    person = Person.query.filter(Person.email==form.data["email"]).first()
    if person is not None:
        user = person.user
    else:
        user = None

    # If there is a user account and person record for this user
    if user is not None and person is not None:
        error = True
        form.email.errors += ['A user with this email address already exists.']

    if len(form.post_code.errors) == 0:
        pc_data = get_postcode_data(form.data["post_code"])
        if not pc_data:
            error = True
            form.post_code.errors += ['The postcode you entered was invalid.']

    if error:
        return render_template('register/yourdetails.html', form=form)

    # If there is a person record but no user account
    if person is None:
        person = Person(
            fname=form.data["first_name"].title(),
            lname=form.data["last_name"].title(),
            email=form.data["email"].lower(),
            post_code=form.data["post_code"].upper(),
            mobile_tel=form.data["tel_no"]
        )

        db.session.add(person)
    else:
        person.first_name = person.first_name or form.data["first_name"].title()
        person.last_name = person.last_name or form.data["last_name"].title()
        person.post_code = person.post_code or form.data["post_code"].upper()
        person.mobile_tel = person.mobile_tel or form.data["tel_no"]

    constituency_id = pc_data["parliamentary_constituency"]
    constituency = Boundary.query.get(constituency_id)
    if constituency is not None:
        person.boundaries.append(constituency)

    ward_id = pc_data["admin_ward"]
    ward = Boundary.query.get(ward_id)
    if ward is not None:
        person.boundaries.append(ward)

    db.session.commit()

    session['person_id'] = person.id

    return redirect(url_for('auth.register', page='Preferences'))


def preferences_handler():
    form = PreferencesForm()

    error = False

    if not form.validate_on_submit():
        error = True

    if error:
        return render_template('register/preferences.html', form=form)

    person = Person.query.get(session["person_id"])

    if form.data["events"]:
        consent = Consent(
            person_id=person.id,
            origin=CONSENT_ORIGINS["registration_form"],
            key=EMAIL_CONSENT_KEYS["email_events"]
        )
        person.consents.append(consent)

    if form.data["messages"]:
        consent = Consent(
            person_id=person.id,
            origin=CONSENT_ORIGINS["registration_form"],
            key=EMAIL_CONSENT_KEYS["email_messages"]
        )
        person.consents.append(consent)

    if form.data["reminders"]:
        consent = Consent(
            person_id=person.id,
            origin=CONSENT_ORIGINS["registration_form"],
            key=EMAIL_CONSENT_KEYS["email_reminders"]
        )
        person.consents.append(consent)

    db.session.commit()

    return redirect(url_for('auth.register', page='Account'))


def account_handler():
    form = AccountForm()

    error = False

    if not form.validate_on_submit() and form.data["wants_account"] == True:
        error = True

    if not error and form.data["password_check"] != form.data["password"]:
        error = True
        form.password_check.errors += ['This must match your chosen password.']

    if error:
        return render_template('register/account.html', form=form, show_password=True)

    if form.data["wants_account"]:
        person = Person.query.get(session["person_id"])
        person.user = User(
            email=person.email,
            password=form.data["password"]
        )

        db.session.commit()

    # Done page
    return redirect(url_for('auth.register', page='Done'))


def get_postcode_data(post_code):
    req = requests.get('https://api.postcodes.io/postcodes/%s' % post_code)

    if req.status_code != 200:
        return False

    data = req.json()

    return data["result"]["codes"]