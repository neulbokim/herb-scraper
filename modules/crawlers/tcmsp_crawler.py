# modules/crawlers/tcmsp_crawler.py

from modules.utils import fetch_with_selenium, save_data, setup_logger
from modules.constants import TCMSP_BASE_URL
from config.settings import TCMSP_RAW_DIR, FILENAME_RULES

logger = setup_logger("tcmsp_crawler")

def crawl_tcmsp(herb_name):
    """
    📝 TCMSP 사이트에서 성분 및 정보 크롤링
    Args:
        herb_name (str): 약재 이름
    """
    logger.info(f"🚀 {herb_name}: TCMSP 크롤링 시작")

    url = f"{TCMSP_BASE_URL}?qr={herb_name}&qsr=herb_en_name"
    ingredients = fetch_with_selenium(url, ".ingredient-link", attribute="href")

    if not ingredients:
        logger.warning(f"⚠️ {herb_name}: 성분 크롤링 실패")
        return

    file_name = FILENAME_RULES["tcmsp_results"].format(herb_name=herb_name)
    save_data(ingredients, file_name, subdir=TCMSP_RAW_DIR)
    logger.info(f"✅ {herb_name}: TCMSP 성분 데이터 저장 완료 → {file_name}")