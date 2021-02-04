import click

from surebets_finder.bet.application.importer import BetImporter
from surebets_finder.bet.application.sure_bets_finder import SureBetsFinder
from surebets_finder.raw_content.aplication.importer import Importer


@click.group()
def cli_group() -> None:
    pass


@cli_group.command()
def import_raw_content() -> None:
    raw_content_importer = Importer()  # type: ignore
    raw_content_importer.import_all()


@cli_group.command()
def import_bets() -> None:
    bet_importer = BetImporter()  # type: ignore
    bet_importer.import_all()


@cli_group.command()
def find_surebets() -> None:
    surebets_finder = SureBetsFinder()  # type: ignore
    surebets_finder.find()


def main() -> None:
    cli = click.CommandCollection(sources=[cli_group])
    cli()


if __name__ == "__main__":
    main()
