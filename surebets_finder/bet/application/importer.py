from logging import Logger

from kink import inject

from surebets_finder.bet.application.bet_finder_factory import BetFinderFactory
from surebets_finder.bet.domain.repositories import BetRepository
from surebets_finder.raw_content.facade import RawContentFacade


@inject
class BetImporter:
    def __init__(self, repository: BetRepository, logger: Logger) -> None:
        self._repository = repository
        self._logger = logger
        self._facade = RawContentFacade()  # type: ignore

    def import_all(self) -> None:
        self._logger.info("Bets importer has started!")

        for raw_content_dto in self._facade.get_all_unprocessed_raw_contents():
            finder = BetFinderFactory.create(raw_content_dto.provider)

            bets = finder.find_bets(raw_content_dto.content, raw_content_dto.category)

            for bet in bets:
                self._repository.create(bet)

            self._logger.info(
                f"Found {len(bets)} from RawContent with id={raw_content_dto.id} where provider={raw_content_dto.provider.value}!"
            )
