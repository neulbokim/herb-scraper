# modules/crawlers/tcmsp_crawler.py

from modules.utils import fetch_with_selenium, save_data, setup_logger
from modules.constants import HERB_URLS  # 변경된 부분: HERB_URLS에서 URL 가져오기
from config.settings import TCMSP_RAW_DIR, FILENAME_RULES

logger = setup_logger("tcmsp_crawler")


def crawl_tcmsp(herb_name):
    """
    📝 TCMSP 사이트에서 성분 및 타겟 정보 크롤링
    """
    logger.info(f"🚀 {herb_name}: TCMSP 크롤링 시작")

    # HERB_URLS에서 herb_name에 해당하는 URL을 가져옴
    url = HERB_URLS.get(herb_name)
    if not url:
        logger.warning(f"⚠️ {herb_name}: URL을 찾을 수 없음")
        return

    ingredient_urls = fetch_with_selenium(url, ".ingredient-link", attribute="href")

    if not ingredient_urls:
        logger.warning(f"⚠️ {herb_name}: 성분 크롤링 실패")
        return

    ingredients = []
    for ingredient_url in ingredient_urls:
        details = fetch_ingredient_details(ingredient_url)
        if details:
            ingredients.append(details)

    if ingredients:
        file_name = FILENAME_RULES["tcmsp_results"].format(herb_name=herb_name)
        save_data(ingredients, file_name, subdir=TCMSP_RAW_DIR)
        logger.info(f"✅ {herb_name}: 성분 데이터 저장 완료 → {file_name}")

    targets = crawl_targets_for_ingredients(ingredients)
    if targets:
        target_file_name = FILENAME_RULES["tcmsp_targets"].format(herb_name=herb_name)
        save_data(targets, target_file_name, subdir=TCMSP_RAW_DIR)
        logger.info(f"✅ {herb_name}: 타겟 데이터 저장 완료 → {target_file_name}")


def fetch_ingredient_details(ingredient_url):
    """📝 성분 상세 페이지에서 mol_id, mol_name 등 정보 크롤링"""
    logger.info(f"🔍 {ingredient_url}: 성분 상세 정보 크롤링 중")

    rows = fetch_with_selenium(ingredient_url, ".ingredient-detail-table tr")
    if not rows:
        logger.warning(f"⚠️ {ingredient_url}: 성분 상세 정보 없음")
        return None

    details = {
        "mol_id": ingredient_url.split('=')[-1],
        "mol_name": rows[0] if rows else "N/A",
        "mol_url": ingredient_url
    }

    return details


def crawl_targets_for_ingredients(ingredients):
    """📝 성분별 타겟 정보 크롤링"""
    targets = []
    for ingredient in ingredients:
        target_data = fetch_targets(ingredient["mol_url"])
        if target_data:
            targets.append({
                "mol_id": ingredient["mol_id"],
                "mol_name": ingredient["mol_name"],
                "targets": target_data
            })
    return targets


def fetch_targets(mol_url):
    """📝 타겟 정보 크롤링"""
    logger.info(f"🔍 {mol_url}: 타겟 크롤링 중")
    rows = fetch_with_selenium(mol_url, "#kendo_target table tbody tr")

    if not rows:
        logger.warning(f"⚠️ {mol_url}: 타겟 정보 없음")
        return []

    targets = []
    for row in rows:
        cols = row.split('\n')
        if len(cols) >= 2:
            targets.append({
                "target_name": cols[0].strip(),
                "target_id": cols[1].strip()
            })

    return targets
