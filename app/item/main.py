from http import HTTPStatus

from flask import request
from flask_restful import MethodView
from pydantic import ValidationError

from app.item.item_model import ItemModel
from app.item.utils import Item
from app.utils import User


class ItemAPI(MethodView):
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

        try:
            validated_item_data = ItemModel(**request.json).dict()
        except ValidationError as val_err:
            return {"message": "Validation error."}, HTTPStatus.BAD_REQUEST

        item = Item(validated_item_data, user)

        # create item document in items collection
        item.create_item_document_in_firestore()

        return item.client_secret
