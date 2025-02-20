# scripts/crawlers/run_batman_tcm_crawler.py

from modules.crawlers.batman_tcm_crawler import crawl_batman_tcm
from modules.constants.herbs import HERB_LIST
from modules.utils import load_from_json, setup_logger
from config.settings import SWISSADME_RAW_DIR

import os

logger = setup_logger("run_batman_tcm_crawler")


def main():
    logger.info("🚀 [BATMAN-TCM API 호출] 시작")

    for herb in HERB_LIST:
        input_file = os.path.join(SWISSADME_RAW_DIR, f"swissadme_results_{herb}.json")
        ingredients = load_from_json(input_file)

        if not ingredients:
            logger.warning(f"⚠️ {herb}: 입력 파일 없음 또는 비어있음 → {input_file}")
            continue

        pubchem_ids = [ing.get("PubChem ID") for ing in ingredients if ing.get("PubChem ID")]
        if not pubchem_ids:
            logger.warning(f"⚠️ {herb}: PubChem ID 없음")
            continue

        logger.info(f"🔬 {herb} BATMAN-TCM 호출 중...")
        crawl_batman_tcm(herb, pubchem_ids)

    logger.info("✅ [BATMAN-TCM API 호출] 완료")


if __name__ == "__main__":
    main()
