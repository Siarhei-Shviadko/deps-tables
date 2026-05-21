import click

from deps_tables.api_app import create_app
from deps_tables.consumer import run_consumer
from deps_tables.extras.web import Application


@click.group()
def cli() -> None:
    pass


@click.command()
def serve() -> None:
    """
    Run web application of OCR service.
    """
    app = create_app()
    Application(app, app.app.config.gunicorn()).run()  # type: ignore[attr-defined]


@click.command()
def consume() -> None:
    run_consumer()


if __name__ == "__main__":
    cli.add_command(serve)
    cli.add_command(consume)
    cli()
