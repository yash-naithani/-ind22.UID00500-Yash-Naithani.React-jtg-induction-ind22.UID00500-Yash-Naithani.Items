from app.helpers import base64UrlDecode
from app.settings import stripe


class Payment:
    def __init__(self, amount: float, currency: str, type: str, id: str) -> None:
        """
        Initializes a Payment object, creates a payment initent.

        Parameter:
            self
            amount float: amount to charge user
            currency str: currency code (Ex: "inr" for Indian Rupee)
        """
        self.payment_intent = stripe.PaymentIntent.create(
            amount=amount,
            currency=currency,
            automatic_payment_methods={"enabled": True},
            metadata={"type": type, "id": id},
        )

        self.client_secret = self.payment_intent.client_secret


class User:
    def __init__(self, request: object) -> None:
        """
        Initializes a user object.

        Parameter:
            self
            request object: Request object
        """
        self.user = base64UrlDecode(request.headers["X-Apigateway-Api-Userinfo"])
