# modules/crawlers/batman_tcm_crawler.py

from modules.utils import fetch_with_api, save_data, setup_logger
from modules.constants import BATMAN_TCM_API_URL
from config.settings import BATMAN_TCM_RAW_DIR, FILENAME_RULES

logger = setup_logger("batman_tcm_crawler")

def crawl_batman_tcm(herb_name, pubchem_ids):
    """
    🧬 BATMAN-TCM API 호출을 통한 타겟 단백질 데이터 수집
    Args:
        herb_name (str): 약재 이름
        pubchem_ids (list): PubChem ID 목록
    """
    logger.info(f"🚀 {herb_name}: BATMAN-TCM API 호출 시작 ({len(pubchem_ids)}개 PubChem ID)")

    results = []
    for pubchem_id in pubchem_ids:
        response = fetch_with_api(BATMAN_TCM_API_URL, params={"pubchem_id": pubchem_id})
        if response:
            results.append({"pubchem_id": pubchem_id, "targets": response})
        else:
            logger.warning(f"⚠️ {pubchem_id}: API 호출 실패")

    file_name = FILENAME_RULES["batman_tcm_results"].format(herb_name=herb_name)
    save_data(results, file_name, subdir=BATMAN_TCM_RAW_DIR)
    logger.info(f"✅ {herb_name}: BATMAN-TCM 결과 저장 완료 → {file_name}")
