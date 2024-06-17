import click

from .. import cli_base


@cli_base.command()
@click.option("-r", "--recursive", is_flag=True, default=False, help="Recursively search for files")
@click.argument("src", type=click.Path(exists=True, writable=True, readable=True, resolve_path=True),
                nargs=-1, required=True)
@click.argument("dst", type=click.Path(writable=True, resolve_path=True, file_okay=False), required=True)
@click.pass_context
def copy(ctx, recursive, src, dst):
    print(recursive, src, dst)
    pass
