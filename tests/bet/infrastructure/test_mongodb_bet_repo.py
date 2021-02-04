from datetime import datetime
from decimal import Decimal
from typing import Any, Dict

import pytest
from bson import Decimal128, ObjectId
from pymongo.database import Database

from surebets_finder.bet.domain.entities import Bet
from surebets_finder.bet.domain.errors import BetNotFoundError
from surebets_finder.bet.infrastructure.mongodb_bet_repo import MongoDBBetRepository
from surebets_finder.shared.category import Category
from surebets_finder.shared.provider import Provider


def test_can_create_bet(mongodb: Database) -> None:
    # given
    repo = MongoDBBetRepository()  # type: ignore

    # and
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
    repo.create(bet)

    # then
    document = mongodb["bet"].find_one({"_id": bet.id})
    assert document["_id"] == bet.id
    assert document["opponent_1"] == bet.opponent_1
    assert document["opponent_2"] == bet.opponent_2


def test_can_get_bet(mongodb: Database) -> None:
    # given
    repo = MongoDBBetRepository()  # type: ignore

    # when
    bet_id = ObjectId()
    mongodb["bet"].insert_one(
        {
            "_id": bet_id,
            "opponent_1": "test 1",
            "opponent_2": "test 2",
            "odds_1": Decimal128("4.12"),
            "odds_2": Decimal128("3.56"),
            "category": Category.ESPORT.value,
            "provider": Provider.EFORTUNA.value,
            "date": datetime.utcnow(),
            "url": "/test/bet/url",
            "updated_at": datetime.utcnow(),
            "created_at": datetime.utcnow(),
        }
    )

    # and
    bet = repo.get(bet_id)

    # then
    assert isinstance(bet, Bet)
    assert bet.id == bet_id
    assert bet.opponent_1 == "test 1"
    assert bet.opponent_2 == "test 2"
    assert bet.odds_1.compare(Decimal(4.12))
    assert bet.odds_2.compare(Decimal(3.56))
    assert bet.url == "/test/bet/url"


def test_get_bet_should_raise_an_exception_when_entity_does_not_exist(mongodb: Database) -> None:
    # given
    repo = MongoDBBetRepository()  # type: ignore

    # then
    with pytest.raises(BetNotFoundError):
        repo.get(ObjectId())


@pytest.mark.usefixtures("fill_in_db_with_bets_which_are_in_future")
def test_get_all_bets_which_are_in_future(mongodb: Database) -> None:
    # given
    repo = MongoDBBetRepository()  # type: ignore

    # when
    in_future = repo.get_all_which_are_in_future()

    # then
    assert len(in_future) == 5


def test_find_one(mongodb: Database, dummy_bet_document: Dict[str, Any]) -> None:
    # given
    repo = MongoDBBetRepository()  # type: ignore

    # when
    bet = repo.find_one(
        {
            "opponent_1": dummy_bet_document["opponent_1"],
            "opponent_2": dummy_bet_document["opponent_2"],
            "date": dummy_bet_document["date"],
        }
    )

    # then
    assert isinstance(bet, Bet)


def test_find_one_should_raise_an_exception_when_there_is_not_such_bet(
    mongodb: Database, dummy_bet_document: Dict[str, Any]
) -> None:
    # given
    repo = MongoDBBetRepository()  # type: ignore

    # then
    with pytest.raises(BetNotFoundError):
        repo.find_one(
            {"opponent_1": "john", "opponent_2": dummy_bet_document["opponent_2"], "date": dummy_bet_document["date"]}
        )


def test_can_save_bet(mongodb: Database, dummy_bet_id: ObjectId) -> None:
    # given
    repo = MongoDBBetRepository()  # type: ignore

    # and
    bet = repo.get(dummy_bet_id)

    # and
    bet.odds_1 = Decimal(6.12)
    bet.url = "another/new/url"

    # when
    repo.save(bet)

    # then
    document = mongodb["bet"].find_one({"_id": bet.id})
    assert str(document["odds_1"]) == str(round(bet.odds_1, 2))
    assert document["url"] == "another/new/url"
