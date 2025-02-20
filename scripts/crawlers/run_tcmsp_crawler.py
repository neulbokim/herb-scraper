# scripts/crawlers/run_tcmsp_crawler.py

from modules.crawlers.tcmsp_crawler import crawl_tcmsp
from modules.constants.herbs import HERB_LIST
from modules.utils import setup_logger

logger = setup_logger("run_tcmsp_crawler")


def main():
    logger.info("🚀 [TCMSP 크롤링] 시작")

    for herb in HERB_LIST:
        logger.info(f"📝 {herb} TCMSP 크롤링 중...")
        crawl_tcmsp(herb)

    logger.info("✅ [TCMSP 크롤링] 완료")


if __name__ == "__main__":
    main()
