from modules.crawlers.herb_crawler import crawl_herb_data
from modules.crawlers.swissadme_crawler import crawl_swissadme
from modules.crawlers.batman_tcm_crawler import crawl_batman_tcm
from modules.crawlers.swisstarget_crawler import crawl_swisstarget
from modules.crawlers.tcmsp_crawler import crawl_tcmsp
# scripts/crawlers/__init__.py

from modules.crawlers import (
    crawl_herb_data,
    crawl_swissadme,
    crawl_batman_tcm,
    crawl_swisstarget,
    crawl_tcmsp
)

__all__ = [
    "crawl_herb_data",
    "crawl_swissadme",
    "crawl_batman_tcm",
    "crawl_swisstarget",
    "crawl_tcmsp",
]
