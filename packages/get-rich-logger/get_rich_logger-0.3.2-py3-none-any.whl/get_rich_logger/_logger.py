from typing import (
    Iterable,
    Literal,
)
from typing_extensions import (
    Unpack,
    TypedDict,
)
from types import ModuleType
import logging
from rich.logging import RichHandler
from rich import traceback


class LoggingBasicConfigExtraKwargs(TypedDict, total=False):
    """
    Optional keyword argument taken from
    [logging.getLogger()](https://docs.python.org/3/library/logging.html)
    excluding `level`, `format`, and `handlers`, and `stream`.
    """
    filename: str | None
    filemode: str
    datefmt: str | None
    style: Literal['%', '{', '$']
    force: bool | None
    encoding: str | None
    errors: str | None


def getRichLogger(
    level: Literal[
        "NOTSET",
        "DEBUG",
        "INFO",
        "WARNING",
        "ERROR",
        "CRITICAL",
    ] | int = "NOTSET",
    name: str | None = None,
    format: str = "%(message)s",
    traceback_show_locals: bool = False,
    traceback_hide_dunder_sunder_locals: bool = True,
    traceback_extra_lines: int = 10,
    traceback_suppressed_modules: Iterable[ModuleType] = (),
    **logging_basic_config_extra_kwargs: Unpack[LoggingBasicConfigExtraKwargs],
) -> logging.Logger:
    """
    Substitute for [logging.getLogger()](https://docs.python.org/3/library/logging.html),
    but pre-configured as rich logger with rich traceback.

    Parameters
    ----------
    level : _Level, optional
        The logging level to use.
        Valid values include "DEBUG", 10, "INFO", 20, "WARNING", 30,
        "ERROR", 40, "CRITICAL", 50.
    name : str, optional
        The name of the logger. Recommended to use `__name__`.
    format : str, optional
        The format string to use for the rich logger.
    traceback_show_locals : bool, optional
        Whether to show local variables in tracebacks.
    traceback_hide_dunder_sunder_locals : bool, optional
        Whether to hide dunder and sunder variables in tracebacks.
        Only applicable to unhandled errors.
    traceback_extra_lines : int, optional
        The number of extra lines to show in tracebacks.
    traceback_suppressed_modules : Iterable[ModuleType], optional
        The modules to suppress in tracebacks (e.g., pandas).
    logging_basic_config_extra_kwargs : Unpack[LoggingBasicConfigExtraKwargs], optional
        Extra keyword arguments to pass to [logging.basicConfig()](https://docs.python.org/3/library/logging.html#logging.basicConfig).

    Returns
    -------
    logging.Logger
        The configured rich logger.

    Raises
    ------
    TypeError
        If additional_handlers is not a logging.Handler,
        Iterable[logging.Handler], or None.

    Examples
    --------
    === "Python"
        ``` python linenums="1"
        import logging
        from get_rich_logger import getRichLogger

        getRichLogger(
            logging_level="DEBUG",
            logger_name=__name__,
            traceback_show_locals=True,
            traceback_extra_lines=10,
            traceback_suppressed_modules=(),
        )

        logging.debug("This is a rich debug message!")  # (1)

        1/0  # (2)
        ```

        1.  Logs will be colored and formatted with rich.
        2.  Unhandled errors will have rich traceback.

    """

    # install rich traceback for unhandled exceptions
    traceback.install(
        extra_lines=traceback_extra_lines,
        theme="monokai",
        show_locals=traceback_show_locals,
        locals_hide_dunder=traceback_hide_dunder_sunder_locals,
        locals_hide_sunder=traceback_hide_dunder_sunder_locals,
        suppress=traceback_suppressed_modules,
    )

    # configure the rich handler
    rich_handler: logging.Handler = RichHandler(
        level=logging.getLevelName(level),
        omit_repeated_times=False,
        rich_tracebacks=True,
        tracebacks_extra_lines=traceback_extra_lines,
        tracebacks_theme="monokai",
        tracebacks_word_wrap=False,
        tracebacks_show_locals=traceback_show_locals,
        tracebacks_suppress=traceback_suppressed_modules,
        log_time_format="[%Y-%m-%d %H:%M:%S] ",
    )

    # configure the logger
    logging.basicConfig(
        level=logging.getLevelName(level),
        format=format,
        handlers=[rich_handler],
        **logging_basic_config_extra_kwargs,
    )

    # return the rich logger
    return logging.getLogger(name)


# ~~~~~ example usage ~~~~~
if __name__ == "__main__":
    logger: logging.Logger = getRichLogger(
        level="DEBUG",
        name=__name__,
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
