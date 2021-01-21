import click

from surebets_finder.raw_content.aplication.importer import Importer


@click.command()
def main() -> None:
    raw_content_importer = Importer()  # type: ignore
    raw_content_importer.import_all()


if __name__ == "__main__":
    main()
