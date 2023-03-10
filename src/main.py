from typing import List, Optional, Tuple
from pydantic import BaseModel, validator


class Bidder(BaseModel):
    name: str
    bids: List[int] = []

    @validator('bids')
    def bids_must_be_nonnegative(cls, v):
        assert all(bid >= 0 for bid in v), 'bids must be nonnegative'
        return v


class Auction(BaseModel):
    bidders: List[Bidder]
    reserve_price: int

    @validator('reserve_price')
    def reserve_price_must_be_nonnegative(cls, v):
        assert v >= 0, 'reserve price must be nonnegative'
        return v

    def find_winner_and_price(self) -> Tuple[Optional[str], Optional[int]]:
        # Initialize variables
        highest_bidder: Optional[str] = None
        highest_bid: int = self.reserve_price
        second_highest_bid: int = self.reserve_price

        # Iterate over all bids
        for bidder in self.bidders:
            # Iterate over all bids from current bidder
            for bid in bidder.bids:
                # Check if bid is above current highest bid and reserve price
                if bid > highest_bid and bid >= self.reserve_price:
                    # Check if highest bidder is not the current bidder
                    if highest_bidder != bidder.name:
                        second_highest_bid = highest_bid
                    highest_bid = bid
                    highest_bidder = bidder.name
                # Check if bid is above current second-highest bid and reserve price
                elif bid > second_highest_bid and bid >= self.reserve_price and highest_bidder != bidder.name:
                    second_highest_bid = bid

        # Check if there is a winner
        if highest_bidder is None:
            return None, None
        else:
            # Compute winning price
            winning_price = second_highest_bid if second_highest_bid > self.reserve_price else self.reserve_price
            return highest_bidder, winning_price
