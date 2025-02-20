# modules/crawlers/swissadme_crawler.py

from modules.utils import fetch_with_selenium, save_data, setup_logger
from config.settings import SWISSADME_RAW_DIR, FILENAME_RULES
from modules.constants import SWISSADME_URL

logger = setup_logger("swissadme_crawler")

def crawl_swissadme(herb_name, ingredients):
    """
    🧪 SwissADME 사이트에서 SMILES 기반 크롤링
    Args:
        herb_name (str): 약재 이름
        ingredients (list): 성분 목록 (SMILES 코드 포함)
    """
    logger.info(f"🚀 {herb_name}: SwissADME 크롤링 시작 ({len(ingredients)}개 성분)")

    results = []
    for ingredient in ingredients:
        smiles = ingredient.get("SMILES")
        if not smiles:
            logger.warning(f"⚠️ {ingredient.get('name', 'Unnamed')}: SMILES 없음 → 건너뜀")
            continue

        data = fetch_with_selenium(SWISSADME_URL, "#smiles", attribute="text")
        results.append({"ingredient": ingredient, "swissadme_data": data})

    file_name = FILENAME_RULES["swissadme_results"].format(herb_name=herb_name)
    save_data(results, file_name, subdir=SWISSADME_RAW_DIR)
    logger.info(f"✅ {herb_name}: SwissADME 결과 저장 완료 → {file_name}")
