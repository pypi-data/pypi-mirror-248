import logging

import click

from vicky.deployment import Deployment

logging.basicConfig(level=logging.INFO)


@click.group()
def cli():
    pass


@click.command()
@click.argument("theme")
@click.argument("directory")
@click.option(
    "--custom_css", default=None, help="path to the file containing custom CSS."
)
@click.option(
    "--custom_js", default=None, help="path to the file containing custom JavaScript."
)
@click.option("--api-key", default=None, help="API key of a Vicky instance.")
@click.option(
    "--version",
    default=None,
    help="version to be set after a successful deployment of a theme.",
)
def deploy(theme, directory, custom_css, custom_js, api_key, version):
    """Deploy a theme to a Vicky instance."""
    deployment = Deployment(
        theme,
        directory,
        custom_css=custom_css,
        custom_js=custom_js,
        api_key=api_key,
        version=version,
    )
    deployment.run()


cli.add_command(deploy)


if __name__ == "__main__":
    cli()
