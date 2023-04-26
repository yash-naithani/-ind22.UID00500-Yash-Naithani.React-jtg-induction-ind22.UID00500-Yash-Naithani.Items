from http import HTTPStatus

from flask import request
from flask_restful import MethodView

from app.payment_webhook.helpers import initialize_hook, validate_request


class PaymentWebhookAPI(MethodView):
    def post(self) -> tuple:
        validated, event = validate_request(request)

        if not validated:
            return {"message": "Unauthorized request."}, HTTPStatus.UNAUTHORIZED

        hook = initialize_hook(event)

        hook.update_status_in_item_document()

        hook.post_process()

        return 200
