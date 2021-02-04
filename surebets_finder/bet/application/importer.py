from logging import Logger

from kink import inject

from surebets_finder.bet.application.bet_finder_factory import BetFinderFactory
from surebets_finder.bet.domain.errors import BetNotFoundError
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
                try:
                    existing_bet = self._repository.find_one(
                        {"opponent_1": bet.opponent_1, "opponent_2": bet.opponent_2, "date": bet.date}
                    )
                    self._logger.info(
                        f"Bet with with params"
                        f"`opponent_1={bet.opponent_1}, opponent_2={bet.opponent_2}, date={bet.date}` "
                        f"already exist! Updating values"
                    )

                    existing_bet.odds_1 = bet.odds_1
                    existing_bet.odds_2 = bet.odds_2
                    existing_bet.url = bet.url
                    self._repository.save(existing_bet)
                except BetNotFoundError:
                    self._logger.info("Creating new bet!")

                    self._repository.create(bet)

            self._facade.mark_raw_content_as_processed(raw_content_dto.id)

            self._logger.info(
                f"Found {len(bets)} from RawContent with id={raw_content_dto.id} where provider={raw_content_dto.provider.value}!"
            )
