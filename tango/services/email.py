import boto3, hashlib, datetime
from botocore.exceptions import ClientError
from flask import current_app

from tango import db
from tango.models.messages import exclusion_list, message_queue
from tango.constants import EMAIL_SENDER, EMAIL_CHARSET, VERIFY_EMAIL
import tango.models.person


def process_email_queue():
    """
    Select any emails waiting on the message queue and take the appropriate action.
    :return: void
    """
    pass


def send_email(to, subject, type, body_text, body_html=None):
    client = boto3.client('ses')

    recipient = tango.models.person.Person.query.filter(tango.models.person.Person.email == to).one()
    if recipient is None:
        return 'E'

    email_hash = hashlib.blake2b()
    email_hash.update(bytes(to, encoding='utf-8'))

    eq = db.select([exclusion_list]).where(db.and_(
        exclusion_list.c.hash == email_hash.hexdigest(),
        exclusion_list.c.until > datetime.datetime.now()
    ))
    exclusions = db.session.execute(eq)
    exclusions = exclusions.fetchall()

    if len(exclusions) > 0 and type != VERIFY_EMAIL:
        return 'X'

    if not recipient.is_email_verified and type != VERIFY_EMAIL:
        return 'X'

    if type is not None and type.len() > 1:
        consent = recipient.check_consent(type)
        if consent is None:
            return 'X'

    # Make sure that if we're in development, we send all emails to the developer
    if current_app.config['FLASK_ENV'] == 'development':
        dev_email = current_app.config['DEV_EMAIL']
    else:
        dev_email = None

    try:
        body = {
            'Text': {
                'Charset': EMAIL_CHARSET,
                'Data': body_text
            }
        }

        if body_html is not None:
            body["Html"] = {
                'Charset': EMAIL_CHARSET,
                'Data': body_html
            }

        response = client.send_email(
            Destination={
                'ToAddresses': [
                    dev_email or recipient.email
                ]
            },
            Message={
                'Body': body,
                'Subject': {
                    'Charset': EMAIL_CHARSET,
                    'Data': subject
                }
            },
            Source=EMAIL_SENDER
        )

    except ClientError as e:
        return 'E'
    else:
        return response['MessageId']


def handle_delivery_notice():
    pass
