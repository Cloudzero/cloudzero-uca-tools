import click


@click.group()  # <- how do i get global options for this command?
@click.pass_context  # Step 2: Add @click.pass_context decorator for context
@click.option("--data", "-d", help="Data to convert")
def cli(ctx, data):
    """Convert Command"""
    # Step 3: ctx.parent to access root scope
    print(ctx.parent.params)
    print(data)


# @cli.group()
# @click.option("--data", "-d", help="Data to convert")
# def convert(data):
#     print(data)

#
#
# @cli.command()
# @click.pass_context
# def convert(ctx):
#     pass
