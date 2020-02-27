from tango.models.messages import exclusion_list, message_queue


def process_email_queue():
    """
    Select any emails waiting on the message queue and take the appropriate action.
    :return: void
    """
    pass


def send_email(person, subject, type, body_text, body_html):
    pass


def handle_delivery_notice():
    pass