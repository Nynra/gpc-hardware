try:
    import piplates.DAQC2plate as DAQC2
except ImportError:
    raise ImportError(
        "piplates.DAQCplate is not installed, are you running on a Raspberry Pi?"
    )
import click


FUNCTION_GENERATOR_CONTEXT = {"DAQC2_ADDR": 0, "DEBUG": False}


@click.group()
@click.option("--debug/--no-debug", default=False)
def function_generator(debug: bool, ctx: dict = FUNCTION_GENERATOR_CONTEXT):
    """Function Generator command group."""
    ctx["DEBUG"] = debug
    if debug:
        click.echo(f"Running function generator with debug = True")

    # Make sure the DAQC2 is connected and in the correct mode
    if not DAQC2.VerifyADDR(ctx["DAQC2_ADDR"]):
        raise ValueError(f"Invalid address: {ctx['DAQC2_ADDR']}")
    if DAQC2.getMode(ctx["DAQC2_ADDR"]) != 0:
        raise ValueError(
            "DAQC2 is not in function generator mode but in {}. ".format(
                DAQC2.getMode(ctx["DAQC2_ADDR"])
            )
        )

@function_generator.command()
@click.argument("channel", type=int)
@click.pass_context
def enable_channel(ctx: dict, channel: int):
    """Enable the function generator."""
    DAQC2.fgON(ctx["DAQC2_ADDR"], channel)
    if ctx["DEBUG"]:
        click.echo(f"Enabled channel {channel}")


@function_generator.command()
@click.argument("channel", type=int)
@click.pass_context
def disable_channel(ctx: dict, channel: int):
    """Disable the function generator channel."""
    DAQC2.fgOFF(ctx["DAQC2_ADDR"], channel)
    if ctx["DEBUG"]:
        click.echo(f"Disabled channel {channel}")


@function_generator.command()
@click.argument("channel", type=int)
@click.argument("waveform", type=str)
@click.pass_context
def set_waveform(ctx: dict, channel: int, waveform: str):
    """Set the waveform of the function generator."""
    DAQC2.fgTYPE(ctx["DAQC2_ADDR"], channel, waveform)
    if ctx["DEBUG"]:
        click.echo(f"Set waveform to {waveform} on channel {channel}")


@function_generator.command()
@click.argument("channel", type=int)
@click.argument("frequency", type=int)
@click.pass_context
def set_frequency(ctx: dict, channel: int, frequency: int):
    """Set the frequency of the function generator."""
    DAQC2.fgFREQ(ctx["DAQC2_ADDR"], channel, frequency)
    if ctx["DEBUG"]:
        click.echo(f"Set frequency to {frequency} on channel {channel}")


@function_generator.command()
@click.argument("channel", type=int)
@click.argument("amplitude", type=int)
@click.pass_context
def set_amplitude(ctx: dict, channel: int, amplitude: int):
    """Set the amplitude of the function generator."""
    DAQC2.fgLEVEL(ctx["DAQC2_ADDR"], channel, amplitude)
    if ctx["DEBUG"]:
        click.echo(f"Set amplitude to {amplitude} on channel {channel}")


@function_generator.command()
@click.pass_context
def emergency_stop(ctx: dict):
    """Stop the function generator."""
    DAQC2.fgOFF(ctx["DAQC2_ADDR"], 0)
    DAQC2.fgOFF(ctx["DAQC2_ADDR"], 1)
    if ctx["DEBUG"]:
        click.echo("Emergency stop")


if __name__ == "__main__":
    function_generator()
