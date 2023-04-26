import sys

from app.constants import PaymentConfig
from app.helpers import amount_to_charge
from app.settings import FS_CLIENT
from app.utils import Payment, User


class Bid(Payment):
    """ """

    def __init__(self, bid_data: dict, image_urls: tuple, user: User) -> None:
        """"""
        self.item_doc = (
            FS_CLIENT.collection("items")
            .document(bid_data["id"])
            .collection("bids")
            .document()
        )

        amount = amount_to_charge(bid_data["amount"])
        # initialising payment
        super().__init__(
            int(amount * 100),
            PaymentConfig.CURRENCY_TYPE.value,
            "bids",
            self.item_doc.id,
        )

        self.data = bid_data
        # adding requester's info
        self.data["bider"] = user.user["user_id"]
        # adding images url
        self.data["images"] = image_urls
        # adding paymet info
        self.data["paymnet_ref"] = self.client_secret

    def create_item_document_in_firestore(self) -> dict:
        """"""
        new_item_doc = self.item_doc.set(self.data)

        return new_item_doc

    def validate_bid(self) -> bool:
        bid = FS_CLIENT.collection("items").document(self.data["id"]).get().to_dict()

        if bid["max_price"] < self.data["amount"]:
            return False
