import os
import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path
import argparse
import configparser

def setup_logging(logfile: str = None, debug: bool = False) -> logging.Logger:
    """
    Configure the logging system

    :param logfile: Path to the logfile.
    :param debug: Boolean indicating whether to enable debug level logging.
    :return: Configured logger instance
    """
    
    if logfile is None:
        initiating_script_dir = os.path.dirname(os.path.abspath(__file__))
        logfile = os.path.join(initiating_script_dir, "script.log")

    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG if debug else logging.INFO)

    log_format = "%(asctime)s %(name)s[%(process)d]: %(levelname)s %(message)s"
    formatter = logging.Formatter(log_format)

    log_path = Path(logfile)
    log_path.parent.mkdir(parents=True, exist_ok=True)

    file_handler = RotatingFileHandler(
        logfile, maxBytes=5 * 1024 * 1024, backupCount=3
    )
    file_handler.setLevel(logging.DEBUG if debug else logging.INFO)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    if debug:
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.DEBUG)
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)
        logger.info("Debugging mode enabled")

    return logger

def get_argument_parser():
    """
    Create and return an argument parser with defautl arguments.
    Additional arguments can be added.

    :return: Configured argparse.ArgumentParser instance
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("--debug", action="store_true", help="Enable debug mode")
    return parser

def get_config(config_file: str = "config.ini"):
    """
    Load and return configuration from the specified config file.

    :param config_file: Path to the config file
    :return: ConfigParser Instance with loaded configurations
    """
    config = configparser.ConfigParser()
    script_dir = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.join(script_dir, config_file)
    config.read(config_path)
    return config
