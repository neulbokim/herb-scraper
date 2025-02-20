# modules/string_api/string_id_fetcher.py

from modules.utils import fetch_with_api, save_to_json, setup_logger
from modules.constants import STRING_ID_API_URL
import os

logger = setup_logger("string_id_fetcher")

def fetch_string_ids(
    gene_names: list,
    species: int = 9606,
    output_file: str = None,
    output_dir: str = None
):
    """
    🆔 STRING API를 사용하여 유전자 이름으로 STRING ID 조회

    Args:
        gene_names (list): 유전자 이름 목록
        species (int): 종(species) 코드 (기본값: 인간 9606)
        output_file (str): 출력 JSON 파일명 (기본: string_id_map.json)
        output_dir (str): 출력 디렉토리 (기본: 현재 경로)
    """
    logger.info(f"🚀 STRING ID 조회 시작: {len(gene_names)}개 유전자")

    results = []
    for gene in gene_names:
        response = fetch_with_api(
            STRING_ID_API_URL, params={"identifiers": gene, "species": species}
        )
        if response:
            results.append({"gene": gene, "string_id": response})
            logger.info(f"✅ {gene}: STRING ID 조회 성공")
        else:
            logger.warning(f"⚠️ {gene}: STRING ID 조회 실패")

    output_dir = output_dir or os.getcwd()
    os.makedirs(output_dir, exist_ok=True)
    output_file = output_file or "string_id_map.json"
    output_path = os.path.join(output_dir, output_file)

    save_to_json(results, output_path)
    logger.info(f"🎯 STRING ID 조회 완료 → {output_path}")
