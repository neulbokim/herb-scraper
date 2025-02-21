# modules/crawlers/herb_crawler.py

from modules.constants.herbs import HERB_URLS
from modules.utils import fetch_with_selenium, save_to_json, setup_logger
from config.settings import HERB_RAW_DIR
from pathlib import Path
import time

logger = setup_logger("herb_crawler")

def crawl_ingredient_details(driver, ingredient_url: str) -> dict:
    """🔍 성분 상세 페이지에서 Molecule Smile 및 Related Gene Targets 추출"""
    base_url = "http://herb.ac.cn"
    full_url = f"{base_url}{ingredient_url}"
    logger.info(f"🔗 성분 상세 페이지 크롤링: {full_url}")

    driver.get(full_url)
    time.sleep(2)

    try:
        smile_element = driver.find_element("xpath", "//b[contains(text(), 'Molecule smile')]/following-sibling::span")
        molecule_smile = smile_element.text.strip()
    except Exception:
        molecule_smile = None
        logger.warning("⚠️ Molecule smile 정보 없음")

    try:
        target_elements = driver.find_elements("xpath", "//h4[contains(text(), 'Related Gene Targets')]/following-sibling::div//li")
        gene_targets = [target.text.strip() for target in target_elements]
    except Exception:
        gene_targets = []
        logger.warning("⚠️ Related Gene Targets 정보 없음")

    return {
        "molecule_smile": molecule_smile,
        "related_gene_targets": gene_targets
    }

def crawl_herb_data(herbs: list):
    """🌿 HERB 크롤링: 약재별 활성 성분 및 타겟 단백질 수집"""
    from modules.utils.web_driver import get_driver

    driver = get_driver(headless=True)

    for herb in herbs:
        herb_url = HERB_URLS.get(herb)
        if not herb_url:
            logger.error(f"❌ {herb}: HERB URL 없음")
            continue

        logger.info(f"🚀 {herb}: 크롤링 시작 → {herb_url}")
        driver.get(herb_url)
        time.sleep(2)

        try:
            ingredient_rows = driver.find_elements("xpath", "//tbody[@class='ant-table-tbody']/tr")
            ingredients = []

            for row in ingredient_rows:
                cells = row.find_elements("tag name", "td")
                if len(cells) >= 3:
                    ingredient_id = cells[0].find_element("tag name", "a").get_attribute("href")
                    ingredient_name = cells[1].text.strip()
                    ingredient_alias = cells[2].text.strip()

                    details = crawl_ingredient_details(driver, ingredient_id)

                    ingredients.append({
                        "ingredient_id": ingredient_id.split("=")[-1],
                        "ingredient_name": ingredient_name,
                        "ingredient_alias": ingredient_alias,
                        "molecule_smile": details["molecule_smile"],
                        "related_gene_targets": details["related_gene_targets"]
                    })

            output_dir = Path(HERB_RAW_DIR)
            output_dir.mkdir(parents=True, exist_ok=True)
            output_path = output_dir / f"herb_ingredient_urls_{herb}.json"
            save_to_json(ingredients, output_path)
            logger.info(f"✅ {herb}: {len(ingredients)}개 성분 수집 완료 → {output_path}")

        except Exception as e:
            logger.error(f"❌ {herb}: 크롤링 실패 - {e}")

    driver.quit()