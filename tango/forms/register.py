from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField

from wtforms.validators import Email, DataRequired, Length


class StartForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    email = StringField('Email', validators=[Email(),DataRequired()])
    post_code = StringField('Post code', validators=[DataRequired(),Length(min=6, max=8)])
    tel_no = StringField('Telephone number', validators=[Length(max=14)])
    submit = SubmitField('Next')


PAGES = {
    'YourDetails': StartForm
}