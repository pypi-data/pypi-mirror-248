"""Asynchronous Python client providing Open Data information of Liège."""


class ODPLiegeError(Exception):
    """Generic Open Data Platform Liège exception."""


class ODPLiegeConnectionError(ODPLiegeError):
    """Open Data Platform Liège - connection error."""
