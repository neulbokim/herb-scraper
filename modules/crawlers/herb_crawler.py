# modules/crawlers/herb_crawler.py

from modules.utils import fetch_with_selenium, save_data, setup_logger
from modules.constants import HERB_URLS
from config.settings import HERB_RAW_DIR, FILENAME_RULES

logger = setup_logger("herb_crawler")

def crawl_herb_data(herb_list=None):
    """
    🌿 HERB 약재 페이지에서 성분 URL 크롤링
    Args:
        herb_list (list): 크롤링할 약재 이름 목록 (None이면 HERB_URLS 전체 사용)
    """
    herb_list = herb_list or HERB_URLS.keys()
    logger.info(f"🚀 HERB 크롤링 시작 ({len(herb_list)}종)")

    for herb_name in herb_list:
        url = HERB_URLS.get(herb_name)
        if not url:
            logger.warning(f"❌ {herb_name}: URL을 찾을 수 없습니다.")
            continue

        logger.info(f"🌿 {herb_name}: URL 크롤링 중 → {url}")
        ingredient_links = fetch_with_selenium(url, ".ingredient-link", attribute="href")

        if not ingredient_links:
            logger.warning(f"⚠️ {herb_name}: 성분 링크 없음")
            continue

        file_name = FILENAME_RULES["herb_ingredient_urls"].format(herb_name=herb_name)
        save_data(ingredient_links, file_name, subdir=HERB_RAW_DIR)
        logger.info(f"✅ {herb_name}: {len(ingredient_links)}개 성분 URL 저장 완료 → {file_name}")

    logger.info("🎉 HERB 크롤링 완료")