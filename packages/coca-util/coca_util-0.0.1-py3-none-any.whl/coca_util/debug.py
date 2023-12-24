# %%
import inspect
from pathlib import Path

__all__ = ["getLocation"]


def getLocation(depth=1):
    """get file path and lineno on Location

    Args:
        depth (int, optional): location depth. Defaults to 1.

    Returns:
        tuple: (file path, lineno)

    Examples:
        >>> def printLocation(msg):
        ...     fname,lineno = getLocation(2)
        ...     print(f"[{fname}:{lineno}]{msg}")
    """
    frame = inspect.stack()[depth]
    return Path(frame.filename), frame.lineno


if __name__ == "__main__":
    import doctest

    doctest.testmod()
