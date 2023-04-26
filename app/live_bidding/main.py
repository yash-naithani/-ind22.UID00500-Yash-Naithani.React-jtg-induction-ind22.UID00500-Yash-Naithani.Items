import sys
from http import HTTPStatus

from flask import request
from flask_restful import MethodView

from app.settings import FS_CLIENT


class LiveBiddingWebhookAPI(MethodView):
    def post(self) -> tuple:
        payload = request.json

        print(payload)
        sys.stdout.flush()

        FS_CLIENT.collection(payload["collection"]).document(payload["id"]).update(
            {"bidding_status": payload["status"]}
        )

        return HTTPStatus.OK
