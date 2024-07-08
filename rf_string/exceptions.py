class RFStringError(Exception):
    """RFString Errors"""


class InconsistentRfStringDefError(RFStringError):
    """RFstr definition is inconsistent."""


class MatchNotFoundError(RFStringError):
    """Match not found for string sample."""
