from http import HTTPStatus

from flask import request
from flask_restful import MethodView
from pydantic import ValidationError

from app.bid.bid_model import BidModel
from app.bid.helpers import upload_images_to_gcs
from app.bid.utils import Bid
from app.utils import User


class BidAPI(MethodView):
    def options(self):
        CORS_HEADERS = {
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "*",
            "Access-Control-Allow-Headers": "*",
            "Access-Control-Max-Age": "3600",
        }

        return ("", 200, CORS_HEADERS)

    def post(self) -> tuple:
        user = User(request)

        form_data = request.form

        bid = {
            "id": form_data.get("id"),
            "amount": form_data.get("amount"),
            "description": form_data.get("description"),
        }

        images = request.files.getlist("images")

        try:
            validated_bid_data = BidModel(**bid).dict()
        except ValidationError as val_err:
            return {"message": "Validation error."}, HTTPStatus.BAD_REQUEST

        if len(images) > 6:
            return {"message": "Images list size error."}, HTTPStatus.BAD_REQUEST

        image_urls = upload_images_to_gcs(images)

        bid = Bid(validated_bid_data, image_urls, user)

        valid_bid = bid.validate_bid()

        if not valid_bid:
            return {"message": "Not a valid bid!"}, HTTPStatus.BAD_REQUEST

        # create item document in items collection
        bid.create_item_document_in_firestore()

        return bid.client_secret
