#!.venv/bin/python
import click

from clicommands.build import build
from clicommands.deploy import deploy
from clicommands.fetch import fetch
from clicommands.update import update


@click.group()
def qscli():
    pass


qscli.add_command(fetch)
qscli.add_command(build)
qscli.add_command(deploy)
qscli.add_command(update)

if __name__ == "__main__":
    qscli()