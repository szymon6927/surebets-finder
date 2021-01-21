from pathlib import Path

import pytest

from surebets_finder.bet.application.bet_finder import BetClickBetFinder, EFortunaBetFinder, LVBetBetFinder
from surebets_finder.bet.domain.entities import Bet
from surebets_finder.shared.category import Category


@pytest.fixture
def efortuna_raw_content() -> str:
    root_project_path = Path(__file__).parent.parent.parent.parent
    file_path = root_project_path / "surebets_finder" / "examples" / "efortuna.html"

    with open(file_path) as file:
        return file.read()


@pytest.fixture
def bet_click_raw_content() -> str:
    root_project_path = Path(__file__).parent.parent.parent.parent
    file_path = root_project_path / "surebets_finder" / "examples" / "betclick.json"

    with open(file_path) as file:
        return file.read()


@pytest.fixture
def lvbet_raw_content() -> str:
    root_project_path = Path(__file__).parent.parent.parent.parent
    file_path = root_project_path / "surebets_finder" / "examples" / "lvbet.json"

    with open(file_path) as file:
        return file.read()


def test_efortuna_bet_finder_correctly_mapping_to_bet_entity(efortuna_raw_content: str) -> None:
    # given
    finder = EFortunaBetFinder()  # type: ignore

    # when
    result = finder.find_bets(efortuna_raw_content, Category.ESPORT)

    # then
    assert isinstance(result[0], Bet)


def test_betclick_bet_finder_correctly_mapping_to_bet_entity(bet_click_raw_content: str) -> None:
    # given
    finder = BetClickBetFinder()  # type: ignore

    # when
    result = finder.find_bets(bet_click_raw_content, Category.ESPORT)

    # then
    assert isinstance(result[0], Bet)


def test_lvbet_bet_finder_correctly_mapping_to_bet_entity(lvbet_raw_content: str) -> None:
    # given
    finder = LVBetBetFinder()  # type: ignore

    # when
    result = finder.find_bets(lvbet_raw_content, Category.ESPORT)

    # then
    assert isinstance(result[0], Bet)
