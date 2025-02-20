# modules/string_api/compound_target_fetcher.py

from modules.utils import fetch_with_api, save_to_json, setup_logger
from modules.constants import COMPOUND_TARGET_API_URL
import os

logger = setup_logger("compound_target_fetcher")

def fetch_compound_targets(
    compounds: list,
    species: int = 9606,
    output_file: str = None,
    output_dir: str = None
):
    """
    🎯 STRING API를 사용하여 화합물-타겟 단백질 매핑

    Args:
        compounds (list): 화합물 목록 (SMILES 또는 이름)
        species (int): 종(species) 코드 (기본값: 인간 9606)
        output_file (str): 출력 JSON 파일명 (기본: compound_targets.json)
        output_dir (str): 출력 디렉토리 (기본: 현재 경로)
    """
    logger.info(f"🚀 화합물-타겟 매핑 시작: {len(compounds)}개 화합물")

    results = []
    for compound in compounds:
        response = fetch_with_api(
            COMPOUND_TARGET_API_URL, params={"compound": compound, "species": species}
        )
        if response:
            results.append({"compound": compound, "targets": response})
            logger.info(f"✅ {compound}: 타겟 조회 성공")
        else:
            logger.warning(f"⚠️ {compound}: 타겟 조회 실패")

    output_dir = output_dir or os.getcwd()
    os.makedirs(output_dir, exist_ok=True)
    output_file = output_file or "compound_targets.json"
    output_path = os.path.join(output_dir, output_file)

    save_to_json(results, output_path)
    logger.info(f"🎯 화합물-타겟 매핑 완료 → {output_path}")
