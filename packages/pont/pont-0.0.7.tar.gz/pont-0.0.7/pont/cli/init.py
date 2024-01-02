import logging

import click

from ..settings import Settings, SettingsError


@click.command()
def init():
    """
    Initialize a pont settings file.
    """
    settings = Settings()
    try:
        settings.init()
        settings.save()
    except SettingsError as error:
        logging.error(error)
        exit(1)
