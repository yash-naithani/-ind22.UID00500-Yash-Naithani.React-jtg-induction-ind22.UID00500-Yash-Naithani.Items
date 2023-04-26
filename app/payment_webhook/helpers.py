import os

import stripe
from dotenv import load_dotenv

from app.payment_webhook.utils import ItemWebhook
from app.settings import FS_CLIENT

load_dotenv()


def validate_request(request) -> tuple:
    payload = request.data
    sig_header = request.headers.get("stripe-signature")

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, os.environ.get("ENDPOINT_SECRET")
        )
        return True, event
    except stripe.error.SignatureVerificationError as e:
        return False, {}


def initialize_hook(event):
    if event["data"]["object"]["metadata"]["type"] == "items":
        return ItemWebhook(event)
    elif event["data"]["object"]["metadata"]["type"] == "bids":
        pass
