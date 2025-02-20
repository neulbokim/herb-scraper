# modules/preprocessors/filter_compounds.py

from modules.utils import load_from_json, save_to_json, setup_logger
import os

logger = setup_logger("filter_compounds")

def filter_active_compounds(
    input_file: str,
    output_file: str = None,
    output_dir: str = None,
    tpsa_threshold: float = 140.0,
    gi_absorption: str = "High"
):
    """
    🧹 활성 성분 필터링 (TPSA 및 GI 흡수 기준)

    Args:
        input_file (str): 입력 JSON 파일 경로
        output_file (str): 출력 JSON 파일명 (기본: 입력 파일명 기반)
        output_dir (str): 출력 디렉토리 (기본: 입력 파일과 동일한 디렉토리)
        tpsa_threshold (float): TPSA 임계값 (기본: 140.0)
        gi_absorption (str): GI 흡수 기준 (기본: "High")
    """
    logger.info(f"🚀 활성 성분 필터링 시작 → {input_file}")

    data = load_from_json(input_file)
    if not data:
        logger.error(f"❌ 입력 파일이 비어있거나 잘못되었습니다: {input_file}")
        return

    filtered = [
        compound for compound in data
        if compound.get("swissadme_data", {}).get("TPSA", 999) <= tpsa_threshold and
           compound.get("swissadme_data", {}).get("GI absorption") == gi_absorption
    ]

    base_name = os.path.splitext(os.path.basename(input_file))[0]
    output_dir = output_dir or os.path.dirname(input_file)
    os.makedirs(output_dir, exist_ok=True)
    output_file = output_file or f"{base_name}_filtered.json"
    output_path = os.path.join(output_dir, output_file)

    save_to_json(filtered, output_path)
    logger.info(f"✅ 필터링 완료: {len(filtered)}개 성분 → {output_path}")
