# scripts/crawlers/run_swisstarget_crawler.py

from modules.crawlers.swisstarget_crawler import crawl_swisstarget
from modules.constants.herbs import HERB_LIST
from modules.utils import load_from_json, setup_logger
from config.settings import SWISSADME_RAW_DIR

import os

logger = setup_logger("run_swisstarget_crawler")


def main():
    logger.info("🚀 [SwissTargetPrediction 크롤링] 시작")

    for herb in HERB_LIST:
        input_file = os.path.join(SWISSADME_RAW_DIR, f"swissadme_results_{herb}.json")
        ingredients = load_from_json(input_file)

        if not ingredients:
            logger.warning(f"⚠️ {herb}: 입력 파일 없음 또는 비어있음 → {input_file}")
            continue

        smiles_list = [ing.get("SMILES") for ing in ingredients if ing.get("SMILES")]
        if not smiles_list:
            logger.warning(f"⚠️ {herb}: SMILES 정보 없음")
            continue

        logger.info(f"🧬 {herb} SwissTargetPrediction 크롤링 중...")
        crawl_swisstarget(herb, smiles_list)

    logger.info("✅ [SwissTargetPrediction 크롤링] 완료")


if __name__ == "__main__":
    main()
