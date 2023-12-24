import functools
import yaml
import os
from typing import Dict, Any, Callable
import logging.handlers

def setup_logger(name: str, caller_file: str, log_dir: str = 'logs') -> logging.Logger:
    """
    Set up a logger with file and console handlers in the specified directory.

    :param name: Name for the logger.
    :param caller_file: File path of the calling script to determine log directory.
    :param log_dir: Directory for log files, defaults to 'logs'.
    :return: Configured logger object.
    """
    # Determine the absolute path to the log directory based on the caller's file location
    base_path = os.path.dirname(os.path.abspath(caller_file))
    log_path = os.path.join(base_path, log_dir)

    # Create the log directory if it doesn't exist
    if not os.path.exists(log_path):
        os.makedirs(log_path)

    # Configure logging
    logger = logging.getLogger(name)
    formatter = logging.Formatter('[%(levelname)s|%(filename)s:%(lineno)s] %(asctime)s > %(message)s')

    # File handler
    fileHandler = logging.FileHandler(os.path.join(log_path, f'{name}.log'))
    fileHandler.setFormatter(formatter)

    # Stream handler (for console output)
    streamHandler = logging.StreamHandler()
    streamHandler.setFormatter(formatter)

    logger.addHandler(fileHandler)
    logger.addHandler(streamHandler)
    logger.setLevel(logging.DEBUG)

    return logger


def load_cofnig(config_file: str) -> Dict[str, Any]:
    """
    Load a YAML configuration file.

    :param config_file: Path to the configuration file.
    :return: Dictionary of configuration values.
    """
    with open(config_file, 'r') as f:
        config = yaml.safe_load(f)

    return config


def cache_func(maxsize: int, func: Callable, *args, **kwargs) -> Any:
    """
    Return a cached version of the specified function.

    :param maxsize: 캐시에 저장할 최대 결과 수.
    :param func: 캐시할 함수.
    :param args: 함수에 전달할 위치 기반 인자들.
    :param kwargs: 함수에 전달할 키워드 기반 인자들.
    :return: 함수의 실행 결과.
    """
    cached_func = functools.lru_cache(maxsize=maxsize)(func)
    return cached_func(*args, **kwargs)
