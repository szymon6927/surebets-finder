from typing import List, Protocol

from typing_extensions import runtime_checkable

from surebets_finder.shared.category import Category
from surebets_finder.shared.reflection import raises


@runtime_checkable
class UrlStrategy(Protocol):
    def get_urls(self) -> List[str]:
        ...


class EFortunaUrlStrategy(UrlStrategy):
    def __init__(self, category: Category) -> None:
        self._category = category

    @raises(ValueError)
    def get_urls(self) -> List[str]:
        if self._category == Category.ESPORT:
            return [
                "https://www.efortuna.pl/zaklady-bukmacherskie/esport-cs-go?selectDates=1",
                "https://www.efortuna.pl/zaklady-bukmacherskie/esport-lol?selectDates=1",
                "https://www.efortuna.pl/zaklady-bukmacherskie/esport-dota2?selectDates=1",
                "https://www.efortuna.pl/zaklady-bukmacherskie/esport-starcraft-2?selectDates=1",
                "https://www.efortuna.pl/zaklady-bukmacherskie/esport-rainbow-six?selectDates=1",
                "https://www.efortuna.pl/zaklady-bukmacherskie/esport-pozosta%C5%82e?selectDates=1",
            ]

        raise ValueError(
            f"Category `{self._category.value}` is not a correct value. Possible value {Category.values()}"
        )


class BetClickUrlStrategy(UrlStrategy):
    def __init__(self, category: Category) -> None:
        self._category = category

    @raises(ValueError)
    def get_urls(self) -> List[str]:
        if self._category == Category.ESPORT:
            return [
                "https://offer.cdn.begmedia.com/api/pub/v4/events?application=2048&countrycode=pl&fetchMultipleDefaultMarkets=true&language=pa&limit=1000&offset=0&sitecode=plpa&sortBy=ByLiveRankingPreliveDate&sportIds=102"
            ]

        raise ValueError(
            f"Category `{self._category.value}` is not a correct value. Possible value {Category.values()}"
        )


class LVBetUrlStrategy(UrlStrategy):
    def __init__(self, category: Category) -> None:
        self._category = category

    @raises(ValueError)
    def get_urls(self) -> List[str]:
        if self._category == Category.ESPORT:
            return [
                "https://app.lvbet.pl/_api/v1/offer/matches/?is_live=false&sports_groups_ids=41592,44058,41604,37221,41575,22686,41588,30309,30496,19045,9152,10023,45661,31949,30934,5878,19835,45642,1168&lang=pl",  # LoL
                "https://app.lvbet.pl/_api/v1/offer/matches/?is_live=false&sports_groups_ids=12007,43200,44564,45586,43555,45676,45719,45721,43673,45336&lang=pl",  # CS GO
                "https://app.lvbet.pl/_api/v1/offer/matches/?is_live=false&sports_groups_ids=2806,45609&lang=pl",  # DOTA
            ]

        raise ValueError(
            f"Category `{self._category.value}` is not a correct value. Possible value {Category.values()}"
        )
