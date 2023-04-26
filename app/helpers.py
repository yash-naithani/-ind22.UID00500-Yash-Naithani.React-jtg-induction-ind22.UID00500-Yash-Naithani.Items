import json
import os
from base64 import urlsafe_b64decode
from datetime import datetime

from dotenv import load_dotenv

from app.settings import CT_CLIENT

load_dotenv()


def base64UrlDecode(base64Url: bytes) -> dict:
    """
    Convering base64url to string.

    Parameter:
        base64url (string): string to decode.
    Returns:
        string
    """
    base64Url = base64Url.encode("utf-8")
    padding = b"=" * (4 - (len(base64Url) % 4))

    return json.loads(urlsafe_b64decode(base64Url + padding).decode("utf-8"))


def amount_to_charge(amount: float) -> float:
    return max(amount / 100.0, 1)


def create_cloud_task(payload: dict, task_name: str, schedule_time: datetime) -> None:
    task = {
        "http_request": {
            "http_method": "POST",
            "url": os.environ.get("LIVEBIDDING_ENDPOINT"),
            "body": json.dumps(payload).encode("utf-8"),
            "headers": {"Content-type": "application/json"},
        },
        "name": CT_CLIENT.task_path(
            os.environ.get("PROJECT_ID"),
            os.environ.get("LOCATION"),
            os.environ.get("QUEUE_NAME"),
            task_name,
        ),
        "schedule_time": schedule_time,
    }

    # Send the task to the Cloud Tasks queue
    response = CT_CLIENT.create_task(
        request={
            "parent": CT_CLIENT.queue_path(
                os.environ.get("PROJECT_ID"),
                os.environ.get("LOCATION"),
                os.environ.get("QUEUE_NAME"),
            ),
            "task": task,
        }
    )
