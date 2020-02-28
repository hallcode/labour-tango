import boto3
from botocore.exceptions import ClientError

from tango.models.messages import exclusion_list, message_queue
from tango.constants import EMAIL_SENDER, EMAIL_CHARSET
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

    if type is not None and type != 'T':
        consent = recipient.check_consent(type)
        if consent is None:
            return 'X'

    if not recipient.is_email_verified and type != 'T':
        return 'X'

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
                    recipient.email
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
        return 'E', e.response["Error"]["Message"]
    else:
        return response['MessageId']


def handle_delivery_notice():
    pass
