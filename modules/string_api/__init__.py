# modules/string_api/__init__.py

from .string_id_fetcher import fetch_string_ids
from .string_ppi_fetcher import fetch_ppi_data
from .compound_target_fetcher import fetch_compound_targets

__all__ = [
    "fetch_string_ids",
    "fetch_ppi_data",
    "fetch_compound_targets",
]
