# modules/utils/__init__.py

from .data_utils import (
    load_from_json,
    save_to_json,
    save_data,
    load_csv,
    save_to_csv,
    save_to_excel,
    file_exists
)
from .web_driver import get_driver
from .logger import setup_logger
from .crawling_utils import fetch_with_selenium, fetch_with_api  # ✅ 직접 가져오기 추가

__all__ = [
    "load_from_json",
    "save_to_json",
    "save_data",
    "load_csv",
    "save_to_csv",
    "save_to_excel",
    "file_exists",
    "get_driver",
    "fetch_with_selenium",  # ✅ 이제 정상 import 가능
    "fetch_with_api",
    "setup_logger",
]
