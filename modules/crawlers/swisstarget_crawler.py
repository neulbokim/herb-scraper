# modules/crawlers/swisstarget_crawler.py

from modules.utils import fetch_with_api, save_data, setup_logger
from modules.constants import SWISSTARGET_URL
from config.settings import SWISSTARGET_RAW_DIR, FILENAME_RULES

logger = setup_logger("swisstarget_crawler")

def crawl_swisstarget(herb_name, smiles_list):
    """
    🎯 SwissTargetPrediction 크롤링 (SMILES 기반)
    Args:
        herb_name (str): 약재 이름
        smiles_list (list): SMILES 목록
    """
    logger.info(f"🚀 {herb_name}: SwissTargetPrediction 크롤링 시작 ({len(smiles_list)}개 SMILES)")

    results = []
    for smiles in smiles_list:
        response = fetch_with_api(SWISSTARGET_URL, params={"smiles": smiles})
        if response:
            results.append({"smiles": smiles, "predictions": response})
        else:
            logger.warning(f"⚠️ {smiles}: 예측 실패")

    file_name = FILENAME_RULES["swisstarget_results"].format(herb_name=herb_name)
    save_data(results, file_name, subdir=SWISSTARGET_RAW_DIR)
    logger.info(f"✅ {herb_name}: SwissTargetPrediction 결과 저장 완료 → {file_name}")
