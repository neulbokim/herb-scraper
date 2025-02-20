# scripts/crawlers/run_swissadme_crawler.py

from modules.crawlers.swissadme_crawler import crawl_swissadme
from modules.constants.herbs import HERB_LIST
from modules.utils import load_from_json, setup_logger
from config.settings import HERB_RAW_DIR

import os

logger = setup_logger("run_swissadme_crawler")


def main():
    logger.info("🚀 [SwissADME 크롤링] 시작")

    for herb in HERB_LIST:
        input_file = os.path.join(HERB_RAW_DIR, f"herb_ingredient_urls_{herb}.json")
        ingredients = load_from_json(input_file)

        if not ingredients:
            logger.warning(f"⚠️ {herb}: 입력 파일 없음 또는 비어있음 → {input_file}")
            continue

        logger.info(f"🧪 {herb} SwissADME 크롤링 중...")
        crawl_swissadme(herb, ingredients)

    logger.info("✅ [SwissADME 크롤링] 완료")


if __name__ == "__main__":
    main()
