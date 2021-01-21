import click

from surebets_finder.bet.application.importer import BetImporter
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


def main() -> None:
    cli = click.CommandCollection(sources=[cli_group])
    cli()


if __name__ == "__main__":
    main()
