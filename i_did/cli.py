"""Tool to keep track of what you did today."""
import datetime

import click

from . import datastore

EDITOR = "vim --cmd ':set tw=79'"

MARKER = (
    "# ------------------------ >8 ------------------------\n"
    "# Do not delete the line above: everything below it will be discarded\n"
    "# Type your message above the line\n"
)


@click.group()
def cli():
    """Keep track of what you did today."""
    datastore.init()


@cli.command()
@click.option("--message", "-m", nargs=1)
def new(message):
    """Add an item to the list of things you've done.

    If no message is given, open vim to get a new message.
    """
    # Get the message to add.
    if not message:
        message = click.edit("\n\n" + MARKER, editor=EDITOR)
        if message is not None:
            message = message.split(MARKER, 1)[0].rstrip("\n")
        if not message:
            click.echo("No message to add", err=True)
            return

    # Add the item to today's file
    datastore.write_item(datetime.datetime.now(), message)
    click.echo("New item added.", err=True)


@cli.command()
@click.option("-v", "--verbose", count=True)
def show(verbose):
    """Show what you've already done this week."""
    today = datetime.datetime.today()

    # Get range of days to show.
    num_days = 7
    days = (today - datetime.timedelta(days=n) for n in range(num_days))

    # Show data for each day.
    for day in days:
        # Get data from file.
        items = datastore.get_items(day)
        if not items:
            continue

        # Format data.
        day_str = day.strftime("%A %B %d, %Y")
        output = f"\n{day_str}\n{'-'*len(day_str)}\n\n"
        items.sort(key=lambda item: item["time"])
        for item in items:
            time = datetime.datetime.fromisoformat(item["time"])
            time_str = click.style(time.strftime("%H:%M"), fg="yellow")
            message_header = item["message"].split("\n", 1)[0]
            output += f"{time_str}  {message_header}" + "\n"
            if verbose:
                message_body = item["message"].split("\n")[1:]
                for line in message_body:
                    output += f"           {line}\n"
                if message_body:
                    output += "\n"

        # Show data.
        click.echo(output)
