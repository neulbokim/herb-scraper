# modules/string_api/string_ppi_fetcher.py

from modules.utils import fetch_with_api, save_to_json, setup_logger
from modules.constants import STRING_PPI_API_URL
import os

logger = setup_logger("string_ppi_fetcher")

def fetch_ppi_data(
    string_ids: list,
    species: int = 9606,
    output_file: str = None,
    output_dir: str = None
):
    """
    🔗 STRING API를 사용하여 PPI 데이터 수집

    Args:
        string_ids (list): STRING ID 목록
        species (int): 종(species) 코드 (기본값: 인간 9606)
        output_file (str): 출력 JSON 파일명 (기본: string_ppi_results.json)
        output_dir (str): 출력 디렉토리 (기본: 현재 경로)
    """
    logger.info(f"🚀 PPI 데이터 수집 시작: {len(string_ids)}개 STRING ID")

    results = []
    for string_id in string_ids:
        response = fetch_with_api(
            STRING_PPI_API_URL, params={"identifiers": string_id, "species": species}
        )
        if response:
            results.append({"string_id": string_id, "ppi_data": response})
            logger.info(f"✅ {string_id}: PPI 데이터 조회 성공")
        else:
            logger.warning(f"⚠️ {string_id}: PPI 데이터 조회 실패")

    output_dir = output_dir or os.getcwd()
    os.makedirs(output_dir, exist_ok=True)
    output_file = output_file or "string_ppi_results.json"
    output_path = os.path.join(output_dir, output_file)

    save_to_json(results, output_path)
    logger.info(f"🎯 PPI 데이터 수집 완료 → {output_path}")
