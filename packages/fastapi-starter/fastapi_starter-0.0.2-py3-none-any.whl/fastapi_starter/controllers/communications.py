"""Communications Controller."""


import json
from os import getenv

import requests

from ..schemas import EmailRecipient
from ..schemas.users import User

FRONTEND_URL = getenv("FRONTEND_URL")
MAILGUN_API_KEY = getenv("MAILGUN_API_KEY")
MAILGUN_DOMAIN_NAME = getenv("MAILGUN_DOMAIN_NAME")
MAILGUN_SENDER_EMAIL = getenv("MAILGUN_SENDER_EMAIL")
MAILGUN_SENDER_NAME = getenv("MAILGUN_SENDER_NAME")


def send_email(
    recipient: EmailRecipient,
    subject: str,
    template: str,
    tags: list[str],
    **args,
):
    """
    Sends an email.

    Parameters
    ----------
        `recipient` (`EmailRecipient`): the recipient to send the email to

        `subject` (`str`): the subject of the email

        `template` (`str`): the Mailgun template for the email's content

        `tags` (`list[str]`): analytic tags to add to the email

        `args` (`dict`): arguments for the template
    """

    return requests.post(
        f"https://api.mailgun.net/v3/{MAILGUN_DOMAIN_NAME}/messages",
        auth=("api", MAILGUN_API_KEY),
        data={
            "from": f"{MAILGUN_SENDER_NAME} <{MAILGUN_SENDER_EMAIL}>",
            "to": f"{recipient.first_name} {recipient.last_name} <{recipient.email}>",
            "subject": subject,
            "template": template,
            "h:X-Mailgun-Variables": json.dumps(args),
            "o:tag": tags,
        },
    )


def send_welcome_email(user: User, token: str):
    return send_email(
        EmailRecipient(
            email=user.username, first_name=user.first_name, last_name=user.last_name
        ),
        "Welcome!",
        "welcome",
        ["welcome"],
        first_name=user.first_name,
        frontend_url=FRONTEND_URL,
        token=token,
    )


def send_password_reset_email(user: User, token: str):
    return send_email(
        EmailRecipient(
            email=user.username, first_name=user.first_name, last_name=user.last_name
        ),
        "Password Reset Requested",
        "password reset",
        ["password-reset"],
        first_name=user.first_name,
        frontend_url=FRONTEND_URL,
        token=token,
    )
