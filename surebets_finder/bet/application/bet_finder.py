import json
from datetime import datetime
from decimal import Decimal
from logging import Logger
from typing import Any, Dict, List, Protocol, Tuple

from bs4 import BeautifulSoup
from bs4.element import Tag
from bson.objectid import ObjectId
from kink import inject

from surebets_finder.bet.domain.entities import Bet
from surebets_finder.shared.category import Category
from surebets_finder.shared.provider import Provider


def _extract_oponents(str_which_contain_two_opponents: str) -> Tuple[str, str]:
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

        return _extract_oponents(opponents_names)

    def _find_odds(self, item: Tag) -> Tuple[Decimal, Decimal]:
        odds = item.select(".odds-value")

        return Decimal(odds[0].text), Decimal(odds[1].text)

    def _find_date(self, item: Tag) -> datetime:
        date_str = item.select_one(".event-datetime").text

        date_str = date_str.replace("\xa0", " ")
        date_str = date_str.strip()

        current_year = datetime.utcnow().strftime("%Y")
        date_str = date_str.replace(" ", current_year)

        return datetime.strptime(date_str, "%d.%m.%Y%H:%M")

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

    def find_bets(self, content: str, category: Category) -> List[Bet]:
        self._logger.info("Finding bets for betclick.pl !")

        json_content = json.loads(content)

        bets = []

        for item in json_content:  # type: Dict[str, Any]
            if item.get("markets"):
                opponent_1 = item["contestants"][0]["name"].lower()
                opponent_2 = item["contestants"][1]["name"].lower()
                odds_1 = Decimal(item["markets"][0]["selections"][0]["odds"])
                odds_2 = Decimal(item["markets"][0]["selections"][1]["odds"])
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

    def find_bets(self, content: str, category: Category) -> List[Bet]:
        self._logger.info("Finding bets for lvbet.pl !")

        json_content = json.loads(content)

        bets = []

        for item in json_content:  # type: Dict[str, Any]
            try:
                opponent_1 = item["participants"]["away"].lower()
                opponent_2 = item["participants"]["home"].lower()
                odds_1 = Decimal(item["primaryMarkets"][0]["selections"][0]["rate"]["decimal"])
                odds_2 = Decimal(item["primaryMarkets"][0]["selections"][1]["rate"]["decimal"])
                date = datetime.fromisoformat(item["date"])

                bet = Bet(
                    id=ObjectId(),
                    opponent_1=opponent_1,
                    opponent_2=opponent_2,
                    odds_1=odds_1,
                    odds_2=odds_2,
                    category=category,
                    provider=Provider.BETCLICK,
                    date=date,
                    url=self._build_url(item, opponent_1, opponent_2),
                    updated_at=datetime.utcnow(),
                )

                bets.append(bet)
            except (IndexError, KeyError) as e:
                self._logger.error(f"Can not fetch all of the information from `{item}` due to {str(e)}.")

        return bets
