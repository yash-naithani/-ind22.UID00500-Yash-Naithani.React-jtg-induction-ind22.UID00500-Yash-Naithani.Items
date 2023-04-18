from flask import request
from flask.views import MethodView
from itemModel import ItemModel
from pydantic import ValidationError


class ItemAPI(MethodView):
    def post():
        item_data = request.json

        try:
            item = ItemModel(item_data)
        except ValidationError as val_err:
            print(val_err)

        return {"data": "hello"}, 200
