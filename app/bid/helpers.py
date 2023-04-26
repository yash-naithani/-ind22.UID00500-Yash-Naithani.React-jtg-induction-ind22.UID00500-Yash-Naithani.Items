import os
from uuid import uuid4

from app.bid.settings import STORAGE_CLIENT


def upload_images_to_gcs(images):
    """Upload a list of images to a Google Cloud Storage bucket."""
    urls = []

    bucket = STORAGE_CLIENT.bucket(os.environ.get("BUCKET_NAME"))

    for image in images:
        filename = str(uuid4())

        blob = bucket.blob(filename)

        blob.upload_from_string(image.read(), content_type=image.content_type)

        urls.append(blob.public_url)

    return urls
