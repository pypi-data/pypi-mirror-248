import click

from .daemon import run, shell, start, stop
from .demo import demo
from .init import init


@click.group()
def cli():
    pass


cli.add_command(demo)
cli.add_command(run)
cli.add_command(start)
cli.add_command(stop)
cli.add_command(shell)
cli.add_command(init)

if __name__ == "__main__":
    cli()
