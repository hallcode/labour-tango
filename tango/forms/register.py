from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField, PasswordField

from wtforms.validators import Email, DataRequired, Length, Regexp, ValidationError


def must_match(other_field, message=None):

    def _must_match(form, field):
        if field.data != other_field.data:
            raise ValidationError(message or 'This field must match %s.' % field)

    return _must_match


class StartForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    email = StringField('Email', validators=[Email(),DataRequired()])
    post_code = StringField('Post code', validators=[DataRequired(),Length(min=6, max=8)])
    tel_no = StringField('Telephone number', validators=[Length(max=14)])
    submit = SubmitField('Next')


class PreferencesForm(FlaskForm):
    events = BooleanField('Event updates and information')
    messages = BooleanField('Messages and important local information')
    reminders = BooleanField('Reminders and prompts')
    submit = SubmitField('Next')


class AccountForm(FlaskForm):
    wants_account = BooleanField('Do you want to set up a user account?')
    password = PasswordField(
        'Password',
        validators=[Regexp(
            regex=r"^.*(?=.{8,})((?=.*[!@#$%^&*()\-_=+{};:,<.>]){1})(?=.*\d)((?=.*[a-z]){1})((?=.*[A-Z]){1}).*$",
            message="Your password did not match the criteria, please make it more complex."
        )]
    )
    password_check = PasswordField('Repeat password')
    submit = SubmitField('Next')


PAGES = {
    'YourDetails': StartForm,
    'Preferences': PreferencesForm,
    'Account': AccountForm
}