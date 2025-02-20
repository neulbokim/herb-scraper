# modules/utils/__init__.py

from .data_utils import (
    load_from_json,
    save_to_json,
    load_csv,
    save_to_csv,
    save_to_excel
)
from .web_driver import get_driver
from .crawling_utils import fetch_with_selenium, fetch_with_api
from .logger import setup_logger

__all__ = [
    "load_from_json",
    "save_to_json",
    "load_csv",
    "save_to_csv",
    "save_to_excel",
    "get_driver",
    "fetch_with_selenium",
    "fetch_with_api",
    "setup_logger",
]
