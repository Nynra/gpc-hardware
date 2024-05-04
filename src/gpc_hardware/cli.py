import click 


@click.group()
def cli(ctx:dict={}):
    # ensure that ctx.obj exists and is a dict (in case `cli()` is called
    # by means other than the `if` block below)
    ctx.ensure_object(dict)

##########################################
# Function Generator
##########################################
@click.group()
def function_generator(ctx:dict={}):
    pass


if __name__ == "__main__":
    cli()