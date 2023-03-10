import pytest
from pydantic import ValidationError
from src.main import Auction, Bidder


def test_auction_with_winner():
    bidders = [
        Bidder(name='A', bids=[110, 130]),
        Bidder(name='B', bids=[]),
        Bidder(name='C', bids=[125]),
        Bidder(name='D', bids=[105, 115, 90]),
        Bidder(name='E', bids=[132, 135, 140])
    ]
    reserve_price = 100
    auction = Auction(bidders=bidders, reserve_price=reserve_price)
    winner, winning_price = auction.find_winner_and_price()
    assert winner == 'E'
    assert winning_price == 135


def test_auction_with_no_winner():
    bidders = [
        Bidder(name=2, bids=[90, 95]),
        Bidder(name='B', bids=[80]),
        Bidder(name='C', bids=[]),
        Bidder(name='D', bids=[85, 80]),
        Bidder(name='E', bids=[])
    ]
    reserve_price = 100
    auction = Auction(bidders=bidders, reserve_price=reserve_price)
    winner, winning_price = auction.find_winner_and_price()
    assert winner is None
    assert winning_price is None


def test_reserve_price_must_be_nonnegative():
    with pytest.raises(ValidationError):
        Auction(bidders=[], reserve_price=-1)


def test_bids_must_be_nonnegative():
    with pytest.raises(ValidationError):
        Bidder(name="A", bids=[-1])


def test_find_winner_and_price_with_winner():
    bidders = [
        Bidder(name="A", bids=[5, 10]),
        Bidder(name="B", bids=[8, 12])
    ]
    auction = Auction(bidders=bidders, reserve_price=5)
    winner, price = auction.find_winner_and_price()
    assert winner == "B"
    assert price == 10


def test_find_winner_and_price_with_tie():
    bidders = [
        Bidder(name="A", bids=[5, 10]),
        Bidder(name="B", bids=[8, 10])
    ]
    auction = Auction(bidders=bidders, reserve_price=5)
    winner, price = auction.find_winner_and_price()
    assert winner == "A"
    assert price == 10
