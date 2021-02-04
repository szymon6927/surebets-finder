from datetime import datetime
from decimal import Decimal

from bson.objectid import ObjectId

from surebets_finder.bet.domain.entities import Bet
from surebets_finder.shared.category import Category
from surebets_finder.shared.provider import Provider


def test_can_instantiate() -> None:
    # given
    bet = Bet(
        id=ObjectId(),
        opponent_1="test 1",
        opponent_2="test 2",
        odds_1=Decimal(4.12),
        odds_2=Decimal(3.56),
        category=Category.ESPORT,
        provider=Provider.EFORTUNA,
        date=datetime.utcnow(),
        url="test/bet/url",
        updated_at=datetime.utcnow(),
    )

    # then
    assert isinstance(bet, Bet)


def test_can_build_full_url_based_on_provider() -> None:
    # given
    bet = Bet(
        id=ObjectId(),
        opponent_1="test 1",
        opponent_2="test 2",
        odds_1=Decimal(4.12),
        odds_2=Decimal(3.56),
        category=Category.ESPORT,
        provider=Provider.EFORTUNA,
        date=datetime.utcnow(),
        url="/test/bet/url",
        updated_at=datetime.utcnow(),
    )

    # when
    full_url = bet.get_full_url()

    # then
    assert full_url == "https://www.efortuna.pl/test/bet/url"


def test_equality_of_two_bets() -> None:
    bet_1 = Bet(
        id=ObjectId(),
        opponent_1="test 1",
        opponent_2="test 2",
        odds_1=Decimal(4.12),
        odds_2=Decimal(3.56),
        category=Category.ESPORT,
        provider=Provider.EFORTUNA,
        date=datetime.utcnow(),
        url="/test/bet/url",
        updated_at=datetime.utcnow(),
    )

    bet_2 = Bet(
        id=ObjectId(),
        opponent_1="test 1",
        opponent_2="test 2",
        odds_1=Decimal(4.12),
        odds_2=Decimal(3.56),
        category=Category.ESPORT,
        provider=Provider.EFORTUNA,
        date=datetime.utcnow(),
        url="/test/bet/url",
        updated_at=datetime.utcnow(),
    )
