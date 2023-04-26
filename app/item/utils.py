from app.constants import PaymentConfig
from app.helpers import amount_to_charge
from app.settings import FS_CLIENT
from app.utils import Payment, User


class Item(Payment):
    """ """

    def __init__(self, item_data: dict, user: User) -> None:
        """"""
        self.item_doc = FS_CLIENT.collection("items").document()

        amount = amount_to_charge(item_data["max_price"])
        # initialising payment
        super().__init__(
            int(amount * 100),
            PaymentConfig.CURRENCY_TYPE.value,
            "items",
            self.item_doc.id,
        )

        self.data = item_data
        # adding requester's info
        self.data["requester"] = user.user["user_id"]
        # adding paymet info
        self.data["paymnet_ref"] = self.client_secret

    def create_item_document_in_firestore(self) -> dict:
        """"""
        new_item_doc = self.item_doc.set(self.data)

        return new_item_doc
