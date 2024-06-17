import click


def start_gui_callback(ctx, _param, value):
    if not value or ctx.resilient_parsing:
        return
    raise NotImplementedError("The GUI is not yet implemented")


@click.group()
@click.option("-b", "--database", required=True, help="DJuiced Database",
              type=click.Path(exists=True, dir_okay=False, writable=False, readable=True))
@click.option("-G", "--gui", is_flag=True, default=False, help="Launch JuicedSerato GUI",
              is_eager=True, expose_value=False, callback=start_gui_callback)
@click.pass_context
def cli_base(ctx, database):
    ctx.ensure_object(dict)
    ctx.obj["DATABASE"] = database


if __name__ == "__main__":
    from .cli import cli_inject

    cli_base()
