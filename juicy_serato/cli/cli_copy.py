import click

from .. import cli_base
from .._juicer import SeratoJuicer


@cli_base.command()
@click.argument("dst", type=click.Path(writable=True, resolve_path=True, file_okay=False), required=True)
@click.pass_context
def copy(ctx, dst):
    database = ctx.obj["DATABASE"]

    with SeratoJuicer(database) as juicer:
        juicer.copy(dst)
        juicer.inject()
