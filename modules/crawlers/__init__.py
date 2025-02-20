# modules/crawlers/__init__.py

from .herb_crawler import crawl_herb_data
from .swissadme_crawler import crawl_swissadme
from .batman_tcm_crawler import crawl_batman_tcm
from .swisstarget_crawler import crawl_swisstarget
from .tcmsp_crawler import crawl_tcmsp

__all__ = [
    "crawl_herb_data",
    "crawl_swissadme",
    "crawl_batman_tcm",
    "crawl_swisstarget",
    "crawl_tcmsp",
]
