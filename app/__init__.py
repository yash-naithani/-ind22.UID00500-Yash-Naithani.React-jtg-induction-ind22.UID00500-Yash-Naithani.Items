from flask import Flask
from flask_cors import CORS
from flask_restful import Api

from app.bid.main import BidAPI
from app.item.main import ItemAPI
from app.live_bidding.main import LiveBiddingWebhookAPI
from app.payment_webhook.main import PaymentWebhookAPI


def create_app() -> Flask:
    app = Flask(__name__)
    api = Api(app)

    CORS(app, resources={r"/*": {"origins": "*"}})

    api.add_resource(ItemAPI, "/item")
    api.add_resource(BidAPI, "/bid")
    api.add_resource(PaymentWebhookAPI, "/webhook")
    api.add_resource(LiveBiddingWebhookAPI, "/livebidding")

    return app
