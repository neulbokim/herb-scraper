from modules.utils import fetch_with_selenium, save_data, setup_logger
from modules.constants import TCMSP_BASE_URL
from config.settings import TCMSP_RAW_DIR, FILENAME_RULES
import time

logger = setup_logger("tcmsp_crawler")

def crawl_tcmsp(herb_name):
    """
    📝 TCMSP 사이트에서 성분 및 타겟 정보 크롤링
    Args:
        herb_name (str): 약재 이름
    """
    logger.info(f"🚀 {herb_name}: TCMSP 크롤링 시작")

    url = f"{TCMSP_BASE_URL}?qr={herb_name}&qsr=herb_en_name"
    ingredients = fetch_with_selenium(url, ".ingredient-link", attribute="href")

    if not ingredients:
        logger.warning(f"⚠️ {herb_name}: 성분 크롤링 실패")
        return

    logger.info(f"✅ {herb_name}: 성분 크롤링 완료 → {len(ingredients)}개 성분 발견")

    # 성분별 상세 페이지 크롤링 (mol_id, mol_name, 타겟 등 포함)
    ingredients_details = []
    for ingredient_url in ingredients:
        ingredient_details = fetch_ingredient_details(ingredient_url)
        if ingredient_details:
            ingredients_details.append(ingredient_details)
    
    if ingredients_details:
        # 성분 데이터 저장
        file_name = FILENAME_RULES["tcmsp_results"].format(herb_name=herb_name)
        save_data(ingredients_details, file_name, subdir=TCMSP_RAW_DIR)
        logger.info(f"✅ {herb_name}: 성분 데이터 저장 완료 → {file_name}")
    
    # 타겟 데이터 크롤링
    targets = crawl_targets_for_ingredients(ingredients_details)
    if targets:
        target_file_name = FILENAME_RULES["tcmsp_results"].format(herb_name=herb_name)
        save_data(targets, target_file_name, subdir=TCMSP_RAW_DIR)
        logger.info(f"✅ {herb_name}: 타겟 데이터 저장 완료 → {target_file_name}")


def fetch_ingredient_details(ingredient_url):
    """
    📝 성분 상세 페이지에서 데이터를 추출
    """
    logger.info(f"🔍 {ingredient_url}: 성분 상세 정보 크롤링 중")
    
    ingredient_details = fetch_with_selenium(ingredient_url, ".ingredient-detail-table tr")
    
    if not ingredient_details:
        logger.warning(f"⚠️ {ingredient_url}: 성분 상세 정보 크롤링 실패")
        return None
    
    # 성분 상세 정보 추출
    details = {
        "mol_id": ingredient_url.split('=')[-1],
        "mol_name": ingredient_details[0].text,  # 예시로 첫 번째 행을 성분명으로 추출
        # 기타 필요한 정보 추가 (예: MolWeight, AlogP 등)
    }
    return details


def crawl_targets_for_ingredients(ingredients_details):
    """
    📝 각 성분에 대한 타겟 크롤링
    """
    targets = []
    for ingredient in ingredients_details:
        mol_url = ingredient["mol_url"]
        target_data = fetch_targets(mol_url)  # 타겟 정보 크롤링
        if target_data:
            targets.append({
                "mol_id": ingredient["mol_id"],
                "mol_name": ingredient["mol_name"],
                "targets": target_data
            })
    
    return targets


def fetch_targets(mol_url):
    """
    📝 성분의 타겟 정보 크롤링
    """
    logger.info(f"🔍 {mol_url}: 타겟 크롤링 중")
    
    target_rows = fetch_with_selenium(mol_url, "#kendo_target table tbody tr")
    
    if not target_rows:
        logger.warning(f"⚠️ {mol_url}: 타겟 크롤링 실패")
        return None
    
    # 타겟 데이터 추출
    targets = []
    for row in target_rows:
        target_name = row.find_element_by_css_selector("td:nth-child(1)").text
        target_id = row.find_element_by_css_selector("td:nth-child(2)").text
        targets.append({
            "target_name": target_name,
            "target_id": target_id
        })
    
    return targets
