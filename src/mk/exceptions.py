class MKUnsupportedOS(Exception):
    """The current operating system is not supported or is invalid."""


class MKInvalidHashHandler(Exception):
    """The HashHandler class must be used within a with-as block."""


class MKInvalidMKName(Exception):
    """The build script must be named exactly "mk.py"!"""
