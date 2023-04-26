"""
Schema for item
"""
from datetime import datetime, timedelta

from pydantic import BaseModel, Field, root_validator, validator

from app.item.constants import EMAIL_VALIDATION_REGEX


class ItemModel(BaseModel):
    """
    Schema for creation of new Item (item requested).
    """

    name: str = Field(min_length=1, max_length=50)
    description: str = Field(min_length=1, max_length=300)
    bidding_time: int
    item_status: str
    max_item_age: int = Field(min=1, max=120)
    items_quantity: int = Field(min=1, max=100)
    max_price: float = Field(min=1, max=10000)

    @validator("item_status")
    def item_status_value(cls, v: str) -> str:
        if v not in ("pre-owned", "new", "refurbished"):
            raise ValueError("Status can only be pre-owned/new/refurbished.")
        return v

    @root_validator
    def check_order_id(cls, values: dict) -> dict:
        # adding live_bidding_time
        values["live_bidding_time"] = datetime.now() + timedelta(
            hours=values["bidding_time"]
        )
        # adding payment status
        values["payment_status"] = "Pending"
        # adding bidding status
        values["bidding_status"] = "Active"
        return values
