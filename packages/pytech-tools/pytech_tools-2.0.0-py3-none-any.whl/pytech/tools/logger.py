import argparse
import datetime
import logging

from logging.handlers import TimedRotatingFileHandler
from pathlib import Path

__all__ = [
    "LoggerHandler",
]


def get_logger_level() -> str:
    """
    Utility function that handles cli arguments.
    If the script is run with the argument
    `-ll=<LOGGER_LEVEL>`
    or
    `--logger-level=<LOGGER_LEVEL>`
    the logger level will be set to <LOGGER_LEVEL>.
    """

    cli_parser = argparse.ArgumentParser()
    cli_parser.add_argument(
        "-ll", "--logger-level",
        default="INFO",
        # logging translates strings to number and vice versa
        # e.g.
        # INFO == 20
        choices=("DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"),
        help="Sets the logger level (default: %(default)s)"
    )
    
    return cli_parser.parse_known_args()[0].logger_level


class AbstractFormatter(logging.Formatter):
    """
    Abstract Formatter for log messages
    """

    msg_format = " - ".join([
        "%(name)s", "%(asctime)s", "%(levelname)s", "%(message)s",
    ])

    level_formats_keys = (
        logging.DEBUG,
        logging.INFO,
        logging.WARNING,
        logging.ERROR,
        logging.CRITICAL,
    )
    level_formats_values = None

    def set_formats(self):
        """
        Method that needs to be implemented in concrete child classes.

        It needs to overwrite the self.level_formats_values with an interable
        of log formatted strings.
        """
        raise NotImplementedError(
            "set_formats method needs to be implemented"
        )

    def get_formats(self) -> dict:
        """
        Method that executes the self.set_formats if 
        self.leve_formats_values == None

        :return: the formats dict
        k == log_level
        v == log_level formatting
        """
        if not self.level_formats_values:
            self.set_formats()

        return {
            k: v for k, v in zip(
                self.level_formats_keys, self.level_formats_values, strict=True
            )
        }

    def format(self, record):
        """
        Function that sets format linked to the level of the record
        """
        log_fmt = self.get_formats().get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)
    

class FileFormatter(AbstractFormatter):
    """
    File Formatter
    """

    def set_formats(self) -> None:
        """
        Method that set the self.level_formats_values
        """
        self.level_formats_values = (
            f"{self.msg_format}",
        ) * len(self.level_formats_keys)
        

class StreamFormatter(AbstractFormatter):
    """
    Stream Formatter
    """

    CYAN = "\x1b[36;20m"
    GREY = "\x1b[38;20m"
    YELLOW = "\x1b[33;20m"
    RED = "\x1b[31;20m"
    BOLD_RED_BG = "\x1b[41;1m"

    colors = (
        CYAN,
        GREY,
        YELLOW,
        RED,
        BOLD_RED_BG,
    )

    RESET = "\x1b[0m"


    def set_formats(self) -> None:
        """
        Method that set the self.level_formats_values
        """
        self.level_formats_values = [
            f"{color}{self.msg_format}{self.RESET}"
            for color in self.colors
        ]


class LoggerHandler:
    """
    Utility class that allows the user to customize the logger name with a
    single <path/filename> log file.

    Basic usage:
    - Create a logger.py file and initialize the LoggerHandler class:

      logger_handler = LoggerHandler()

    - Import the logger_handler in each file that will log messages and assign
      the result of logger_handler.get_logger(__name__) to the logger variable:

      from logger import logger_handler
      
      logger = logger_handler.get_logger(__name__)

    - Log messages with the logging.Logger methods:
      - logger.debug(<msg>)
      - logger.info(<msg>)
      - logger.warning(<msg>)
      - logger.error(<msg>)
      - logger.critical(<msg>)
    """

    def __init__(self, filename: str = "app.log", path: str = "logs") -> None:
        """
        Class initialization

        :param filename: the log filename
        :param path: the log file's path
        """
        self.filename = filename

        try:
            self.path = Path(path)
        except TypeError:
            self.path = Path("logs")
        finally:
            if not self.path.exists():
                Path.mkdir(self.path)

    def get_logger(self, logger_name: str = __name__) -> logging.Logger:
        """
        Function that initializes the logger, set the log rotation,
        configures the file_handler and stream_handler.

        :param logger_name: the logger name
        :return: a logging.Logger instance
        """
        logger_level = get_logger_level()

        logger = logging.getLogger(logger_name)
        logger.setLevel(logger_level)
        file_handler = TimedRotatingFileHandler(
            filename=Path.joinpath(self.path, self.filename),
            when="W6", # run each sunday
            atTime=datetime.time(23), # at 23:00
            backupCount=10 # and rotate after 10 weeks
        )
        file_handler.setFormatter(FileFormatter())
        file_handler.setLevel(logger_level)

        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(StreamFormatter())
        stream_handler.setLevel(logger_level)

        logger.addHandler(file_handler)
        logger.addHandler(stream_handler)

        return logger

if __name__ == "__main__":
    logger_handler = LoggerHandler()
    logger = logger_handler.get_logger()
    logger.setLevel(logging.DEBUG)
    logger.debug("Hi from the logger package")
    logger.info("Hi from the logger package")
    logger.warning("Hi from the logger package")
    logger.error("Hi from the logger package")
    logger.critical("Hi from the logger package")
