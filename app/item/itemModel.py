"""
Schema for item
"""
from datetime import datetime, timedelta

from pydantic import BaseModel, Field


class ItemModel(BaseModel):
    """
    Schema for creation of new Item (item requested).
    """

    name: str
    description: str
    requester: str
    data_and_time: datetime
    item_status: str
    max_item_age: int
    items_quantity: int
    max_price: int

    live_bidding_starts: datetime = Field(
        default_factory=datetime.now + timedelta(hours=9)
    )
