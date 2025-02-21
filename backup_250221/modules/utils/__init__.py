# modules/utils/__init__.py

from .data_utils import (
    load_from_json,
    save_to_json,
    save_to_csv,
    save_to_excel,
    save_data,
)
from .web_driver import get_driver
from .logger import setup_logger
from .crawling_utils import fetch_with_selenium

