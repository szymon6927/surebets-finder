import json
from datetime import datetime
from decimal import Decimal
from logging import Logger
from typing import Any, Dict, List, Protocol, Tuple

import pytz
from bs4 import BeautifulSoup
from bs4.element import Tag
from bson.objectid import ObjectId
from kink import inject

from surebets_finder.bet.domain.entities import Bet
from surebets_finder.shared.category import Category
from surebets_finder.shared.provider import Provider
from surebets_finder.shared.reflection import raises


def _extract_opponents(str_which_contain_two_opponents: str) -> Tuple[str, str]:
    without_white_spaces = " ".join(str_which_contain_two_opponents.split())

    splited = without_white_spaces.split(" ")
    index = splited.index("-")

    opponent_1_parts = []
    opponent_2_parts = []
    for i, item in enumerate(splited):
        if i < index:
            opponent_1_parts.append(item)

        if i > index:
            opponent_2_parts.append(item)

    opponent_1 = " ".join(opponent_1_parts)
    opponent_2 = " ".join(opponent_2_parts)

    return opponent_1.lower().strip(), opponent_2.lower().strip()


class BetFinder(Protocol):
    def find_bets(self, content: str, category: Category) -> List[Bet]:
        ...


@inject
class EFortunaBetFinder(BetFinder):
    def __init__(self, logger: Logger) -> None:
        self._logger = logger

    def _find_oponents(self, item: Tag) -> Tuple[str, str]:
        opponents_names = item.select_one(".market-name").text
        opponents_names = opponents_names.strip()

        return _extract_opponents(opponents_names)

    def _find_odds(self, item: Tag) -> Tuple[Decimal, Decimal]:
        odds = item.select(".odds-value")

        return Decimal(odds[0].text), Decimal(odds[1].text)

    def _find_date(self, item: Tag) -> datetime:
        date_str = item.select_one(".event-datetime").text

        date_str = date_str.replace("\xa0", " ")
        date_str = date_str.strip()

        current_year = datetime.utcnow().strftime("%Y")
        date_str = date_str.replace(" ", current_year)

        data_time_obj = datetime.strptime(date_str, "%d.%m.%Y%H:%M")
        timezone = pytz.timezone("Europe/Warsaw")

        data_time_obj_with_timezone = timezone.localize(data_time_obj)

        return data_time_obj_with_timezone.astimezone(pytz.utc)

    def _find_url(self, item: Tag) -> str:
        url_html_tag = item.select_one("a.event-name")

        return url_html_tag.get("href", "")

    def find_bets(self, content: str, category: Category) -> List[Bet]:
        self._logger.info("Finding bets for efortuna.pl !")

        bets = []

        parsed_content = BeautifulSoup(content, "html.parser")

        for item in parsed_content.select("table tbody tr"):  # type: Tag
            if "running-live" in item.get("class", []):
                self._logger.info(f"HTML item `{item}` has class `running-live`, skiping this one!")
                continue

            if "row-sub-markets" in item.get("class", []):
                self._logger.info(f"HTML item `{item}` has class `row-sub-markets`, skiping this one!")
                continue

            try:
                opponent_1, opponent_2 = self._find_oponents(item)
                odds_1, odds_2 = self._find_odds(item)
                date = self._find_date(item)
                url = self._find_url(item)

                bet = Bet(
                    id=ObjectId(),
                    opponent_1=opponent_1,
                    opponent_2=opponent_2,
                    odds_1=odds_1,
                    odds_2=odds_2,
                    category=category,
                    provider=Provider.EFORTUNA,
                    date=date,
                    url=url,
                    updated_at=datetime.utcnow(),
                )

                bets.append(bet)
            except (IndexError, AttributeError, ValueError) as e:
                self._logger.error(f"Can not fetch all of the information from `{item}` due to {str(e)}.")

        return bets


@inject
class BetClickBetFinder(BetFinder):
    def __init__(self, logger: Logger) -> None:
        self._logger = logger

    @raises(ValueError)
    def _find_odds_1(self, item: Dict[str, Any]) -> Decimal:
        opponent_1 = item["contestants"][0]["shortName"]
        for selection in item["markets"][0]["selections"]:
            if selection["name"] == opponent_1:
                return Decimal(selection["odds"])

        raise ValueError(f"Can not find odds1!")

    @raises(ValueError)
    def _find_odds_2(self, item: Dict[str, Any]) -> Decimal:
        opponent_2 = item["contestants"][1]["shortName"]
        for selection in item["markets"][0]["selections"]:
            if selection["name"] == opponent_2:
                return Decimal(selection["odds"])

        raise ValueError(f"Can not find odds2!")

    def find_bets(self, content: str, category: Category) -> List[Bet]:
        self._logger.info("Finding bets for betclick.pl !")

        json_content = json.loads(content)

        bets = []

        for item in json_content:  # type: Dict[str, Any]
            try:
                if item.get("markets"):
                    opponent_1 = item["contestants"][0]["name"].lower()
                    opponent_2 = item["contestants"][1]["name"].lower()
                    odds_1 = self._find_odds_1(item)
                    odds_2 = self._find_odds_2(item)
                    date = datetime.strptime(item["date"], "%Y-%m-%dT%H:%M:%SZ")
                    url = f'{item["competition"]["relativeDesktopUrl"]}/{item["relativeDesktopUrl"]}'

                    bet = Bet(
                        id=ObjectId(),
                        opponent_1=opponent_1,
                        opponent_2=opponent_2,
                        odds_1=odds_1,
                        odds_2=odds_2,
                        category=category,
                        provider=Provider.BETCLICK,
                        date=date,
                        url=url,
                        updated_at=datetime.utcnow(),
                    )

                    bets.append(bet)
            except ValueError as e:
                self._logger.error(f"Can not fetch all of the information from `{item}` due to {str(e)}.")

        return bets


@inject
class LVBetBetFinder(BetFinder):
    def __init__(self, logger: Logger) -> None:
        self._logger = logger

    def _build_url(self, item: Dict[str, Any], opponent_1: str, opponent_2: str) -> str:
        url_parts = []
        ids = []

        for row in item["sportsGroups"]:
            url_partial_id = row["id"]
            label = row["label"]

            url_parts.append(label)
            ids.append(str(url_partial_id))

        url_parts.append(f"{opponent_1.replace(' ', '-')}-vs-{opponent_2.replace(' ', '-')}")

        first_part_of_url = "/".join(url_parts)
        ids_part_of_url = "/".join(ids)

        return f'{first_part_of_url}/--/{ids_part_of_url}/{item["id"]}'

    @raises(ValueError)
    def _find_odds_1(self, item: Dict[str, Any]) -> Decimal:
        opponent_1 = item["participants"]["home"]

        for selection in item["primaryMarkets"][0]["selections"]:
            if selection["name"] == opponent_1:
                return Decimal(selection["rate"]["decimal"])

        raise ValueError(f"Can not find odds1!")

    @raises(ValueError)
    def _find_odds_2(self, item: Dict[str, Any]) -> Decimal:
        opponent_2 = item["participants"]["away"]

        for selection in item["primaryMarkets"][0]["selections"]:
            if selection["name"] == opponent_2:
                return Decimal(selection["rate"]["decimal"])

        raise ValueError(f"Can not find odds12")

    def find_bets(self, content: str, category: Category) -> List[Bet]:
        self._logger.info("Finding bets for lvbet.pl !")

        json_content = json.loads(content)

        bets = []

        for item in json_content:  # type: Dict[str, Any]
            try:
                opponent_1 = item["participants"]["home"].lower()
                opponent_2 = item["participants"]["away"].lower()
                odds_1 = self._find_odds_1(item)
                odds_2 = self._find_odds_2(item)
                date = datetime.fromisoformat(item["date"])

                bet = Bet(
                    id=ObjectId(),
                    opponent_1=opponent_1,
                    opponent_2=opponent_2,
                    odds_1=odds_1,
                    odds_2=odds_2,
                    category=category,
                    provider=Provider.LVBET,
                    date=date,
                    url=self._build_url(item, opponent_1, opponent_2),
                    updated_at=datetime.utcnow(),
                )

                bets.append(bet)
            except (IndexError, KeyError, ValueError) as e:
                self._logger.error(f"Can not fetch all of the information from `{item}` due to {str(e)}.")

        return bets
