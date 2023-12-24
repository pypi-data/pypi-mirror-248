import typer

cli = typer.Typer()

@cli.command()
def run():
    """
    Launch the app
    """
    from .demo import launch
    launch()

@cli.command()
def init():
    """
    Initialize the GHScout environment
    """
    print("Initializing GHScout environment...")

@cli.callback(no_args_is_help=True)
def main(ctx: typer.Context):
    """
    """
