import click

from .. import cli_base


@cli_base.command()
@click.option("-r", "--recursive", is_flag=True, default=False, help="Recursively search for files")
@click.argument("src", type=click.Path(exists=True, writable=True, readable=True, resolve_path=True),
                nargs=-1, required=True)
@click.pass_context
def inject(ctx, recursive, src):
    print(recursive, src)
    pass
