class PURCError(Exception):
    """Base PURC exception."""


class PURCConnectionError(
    PURCError
):
    """Website unavailable."""


class PURCParseError(
    PURCError
):
    """Unexpected HTML format."""