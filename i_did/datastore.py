"""Datastore for i-did.

This datastore uses a JSON file-based system.
"""
import json
from pathlib import Path

from . import utils

STORE_DIR = Path("~/.i-did").expanduser()


def init():
    """Ensure the datastore is configured."""
    # Make sure the directory for storing files exists.
    if not STORE_DIR.is_dir():
        assert (
            not STORE_DIR.exists()
        ), f"{STORE_DIR} already exists but is not a directory"
        STORE_DIR.mkdir()


def get_items(timestamp):
    """Read items from the datastore for a particular date.

    Args:
        timestamp (datetime.datetime): Date of the items to retrieve.

    Returns:
        list of items from the given date.

    """
    fpath = _get_fpath(timestamp)

    if not fpath.exists():
        return []

    with fpath.open() as fd:
        data = json.loads(fd.read())
    return data["items"]


def write_item(timestamp, message):
    """Add an item to the datastore.

    Args:
        timestamp (datetime.datetime): The timestamp of the new message.
        message (str): The message to save.

    """
    # Format message.
    message = utils.remove_extra_newlines(message)

    # Create new item to save.
    new_item = new_item = {
        "message": message,
        "time": timestamp.isoformat(),
    }

    # Append item to existing list.
    items = get_items(timestamp)
    items.append(new_item)

    # Write data to file.
    fpath = _get_fpath(timestamp)
    with fpath.open("w") as fd:
        json.dump({"items": items}, fd)


def _get_fpath(timestamp):
    """Get the filepath for a given date/time.

    Args:
        timestamp (datetime.datetime): The time/date to get the path for.

    Returns:
        pathlib.Path object for the JSON file for that date.

    """
    fname = f"{timestamp.date().isoformat()}.json"
    return STORE_DIR.joinpath(fname)
