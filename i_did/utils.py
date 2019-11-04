"""Formatting helpers for i-did."""


def remove_extra_newlines(message):
    """Limit the number of newlines in a message to 2."""
    while "\n\n\n" in message:
        message = message.replace("\n\n\n", "\n\n")
    return message
