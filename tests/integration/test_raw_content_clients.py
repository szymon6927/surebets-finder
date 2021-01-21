import pytest

from surebets_finder.raw_content.aplication.clients.betclick_client import BetClickClient
from surebets_finder.raw_content.aplication.clients.efortuna_client import EFortunaClient
from surebets_finder.raw_content.aplication.clients.lvbet_client import LvBetClient


@pytest.mark.slow
def test_efortuna_client_can_fetch_raw_data() -> None:
    # given
    client = EFortunaClient(urls=["https://www.efortuna.pl/zaklady-bukmacherskie/mma/ksw#"])  # type: ignore

    # when
    raw_html_content = client.get_raw_data()

    # then
    assert "main-content" in raw_html_content


@pytest.mark.slow
def test_betclick_client_can_fetch_raw_data() -> None:
    # given
    client = BetClickClient(
        urls=[
            "https://offer.cdn.begmedia.com/api/pub/v4/events?application=2048&countrycode=pl&fetchMultipleDefaultMarkets=true&language=pa&limit=1000&offset=0&sitecode=plpa&sortBy=ByLiveRankingPreliveDate&sportIds=16"
        ]
    )  # type: ignore

    # when
    raw_content = client.get_raw_data()

    # then
    assert "selections" in raw_content


@pytest.mark.slow
def test_lvbet_client_can_fetch_raw_data() -> None:
    # given
    client = LvBetClient(
        urls=["https://app.lvbet.pl/_api/v1/offer/matches/?is_live=false&sports_groups_ids=683&lang=pl"]
    )  # type: ignore

    # when
    raw_content = client.get_raw_data()

    # then
    assert "selections" in raw_content
