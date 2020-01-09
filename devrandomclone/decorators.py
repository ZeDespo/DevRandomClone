from functools import wraps
from time import time
from typing import Callable


def validate_reddit_token(method: Callable) -> Callable:
    """
    Wrapper for devrandomclone's reddit functionality. Verifies if the entropy generating function still has a valid
    token to access reddit. If it does not, grab a new one.
    :param method: The entropy generating function
    :return: The embedded wrapper for the function
    """
    @wraps(method)
    def wrapper(self, *args, **kwargs) -> None:
        now = int(time())
        if now >= self.expiry:
            self.headers, self.expiry = self._reddit_access_token()
        method(self, *args, **kwargs)
    return wrapper
