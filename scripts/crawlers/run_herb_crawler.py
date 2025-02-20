# scripts/crawlers/run_herb_crawler.py

from modules.crawlers.herb_crawler import crawl_herb_data
from modules.constants.herbs import HERB_LIST
from modules.utils import setup_logger

logger = setup_logger("run_herb_crawler")


def main():
    logger.info("🚀 [HERB 크롤링] 시작")

    for herb in HERB_LIST:
        logger.info(f"🌿 {herb} 크롤링 중...")
        crawl_herb_data(herb)

    logger.info("✅ [HERB 크롤링] 완료")


if __name__ == "__main__":
    main()
