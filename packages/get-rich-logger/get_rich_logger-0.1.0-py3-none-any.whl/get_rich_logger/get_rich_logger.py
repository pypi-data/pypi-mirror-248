from typing import Iterable
from types import ModuleType
import logging
from rich.logging import RichHandler
from rich import traceback


def getRichLogger(
    logging_level: str | int = "NOTSET",
    logger_name: str | None = None,
    format: str = "%(message)s",
    traceback_show_locals: bool = False,
    traceback_hide_dunder_locals: bool = True,
    traceback_hide_sunder_locals: bool = True,
    traceback_extra_lines: int = 10,
    traceback_suppressed_modules: Iterable[ModuleType] = (),
) -> logging.Logger:
    """
    Substitute for logging.getLogger(), but pre-configured as rich logger
    with rich traceback.

    Parameters
    ----------
    logging_level : str or int, optional
        The logging level to use. Defaults to 'NOTSET'.
    logger_name : str, optional
        The name of the logger. Defaults to None.
    format : str, optional
        The format string to use for the rich logger.
        Defaults to '%(message)s'.
    traceback_show_locals : bool, optional
        Whether to show local variables in tracebacks. Defaults to False.
    traceback_hide_dunder_locals : bool, optional
        Whether to hide dunder variables in tracebacks. Defaults to True.
    traceback_hide_sunder_locals : bool, optional
        Whether to hide sunder variables in tracebacks. Defaults to True.
    traceback_extra_lines : int, optional
        The number of extra lines to show in tracebacks. Defaults to 10.
    traceback_suppressed_modules : Iterable[ModuleType], optional
        The modules to suppress in tracebacks (e.g., pandas).
        Defaults to ().

    Returns
    -------
    logging.Logger
        The configured logger.

    Raises
    ------
    TypeError
        If additional_handlers is not a logging.Handler,
        Iterable[logging.Handler], or None.

    Example
    -------
    >>> import logging
    >>> from logger import getRichLogger
    >>> getRichLogger(
            logging_level="DEBUG",
            logger_name=__name__,
            traceback_show_locals=True,
            traceback_extra_lines=10,
            traceback_suppressed_modules=(),
        )
    >>> logging.debug("This is a rich debug message!")
    >>> 1/0
    """

    # install rich traceback for unhandled exceptions
    traceback.install(
        extra_lines=traceback_extra_lines,
        theme="monokai",
        show_locals=traceback_show_locals,
        locals_hide_dunder=traceback_hide_dunder_locals,
        locals_hide_sunder=traceback_hide_sunder_locals,
        suppress=traceback_suppressed_modules,
    )

    # configure the rich handler
    rich_handler: logging.Handler = RichHandler(
        level=logging.getLevelName(logging_level),
        omit_repeated_times=False,
        rich_tracebacks=True,
        tracebacks_extra_lines=traceback_extra_lines,
        tracebacks_theme="monokai",
        tracebacks_word_wrap=False,
        tracebacks_show_locals=traceback_show_locals,
        tracebacks_suppress=traceback_suppressed_modules,
        log_time_format="[%Y-%m-%d %H:%M:%S] ",
    )

    logging.basicConfig(
        level=logging.getLevelName(logging_level),
        format=format,
        handlers=[rich_handler],
    )

    return logging.getLogger(logger_name)


# ~~~~~ example usage ~~~~~
if __name__ == "__main__":
    logger: logging.Logger = getRichLogger(
        logging_level="DEBUG",
        logger_name=__name__,
    )

    # # Gives rich traceback for unhandled errors
    # 1/0

    # Also gives rich traceback for handled exceptions
    try:
        1 / 0
    except Exception as e:
        logger.exception(
            "This is an example rich logger error message for handled"
            f"exception! Error: {e}"
        )
