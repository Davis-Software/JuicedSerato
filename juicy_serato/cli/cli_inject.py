import click

from .. import cli_base
from .._juicer import SeratoJuicer


@cli_base.command()
@click.pass_context
def inject(ctx):
    database = ctx.obj["DATABASE"]

    with SeratoJuicer(database) as juicer:
        juicer.inject()
