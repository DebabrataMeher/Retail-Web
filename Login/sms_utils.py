# sms_utils.py

# from twilio.rest import Client
from django.conf import settings
from twilio.rest import Client

def send_sms(to_phone_number, message):
    account_sid = settings.TWILIO_ACCOUNT_SID
    auth_token = settings.TWILIO_AUTH_TOKEN
    twilio_phone_number = settings.TWILIO_PHONE_NUMBER

    client = Client(account_sid, auth_token)

    client.messages.create(
        body=message,
        from_=twilio_phone_number,
        to=to_phone_number
    )
