"""
Schema for Bid
"""
from pydantic import BaseModel, Field, validator


class BidModel(BaseModel):
    """
    Schema for creation of new Bid (item bid).
    """

    id: str
    amount: float = Field(min=1, max=10000)
    description: str = Field(min_length=1, max_length=300)
