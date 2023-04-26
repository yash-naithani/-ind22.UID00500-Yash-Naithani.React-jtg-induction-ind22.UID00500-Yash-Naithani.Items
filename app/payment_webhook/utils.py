from datetime import timedelta

from app.helpers import create_cloud_task
from app.settings import FS_CLIENT


class Webhook:
    def __init__(self, event):
        self.event = event
        # firestore related information
        self.firestore_collection = event["data"]["object"]["metadata"]["type"]
        self.doc_id = event["data"]["object"]["metadata"]["id"]

    def update_status_in_item_document(self):
        FS_CLIENT.collection(self.firestore_collection).document(self.doc_id).update(
            {"payment_status": self.event["type"]}
        )

    def get_resource_doc(self) -> dict:
        return (
            FS_CLIENT.collection(self.firestore_collection)
            .document(self.doc_id)
            .get()
            .to_dict()
        )

    def post_process(self):
        pass


class ItemWebhook(Webhook):
    def __init__(self, event) -> None:
        super().__init__(event)

    def post_process(self) -> None:
        item_doc = self.get_resource_doc()

        live_bidding_payload = {
            "id": self.doc_id,
            "collection": self.firestore_collection,
            "status": "live",  # mark bidding_status to live
        }

        # create cloud task
        create_cloud_task(
            live_bidding_payload,
            f"live_{self.doc_id}",
            item_doc["live_bidding_time"],  # check attr name
        )

        close_bidding_payload = {
            "id": self.doc_id,
            "collection": self.firestore_collection,
            "status": "close",  # mark bidding_status to close
        }

        # create cloud task
        create_cloud_task(
            close_bidding_payload,
            f"close_{self.doc_id}",
            item_doc["live_bidding_time"] + timedelta(hours=1),  # check attr name
        )
