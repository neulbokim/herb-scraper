# modules/preprocessors/merge_herb_data.py

from modules.utils import load_from_json, save_to_json, setup_logger
import os

logger = setup_logger("merge_herb_data")

def merge_herb_data(
    herb_data_file: str,
    swissadme_file: str,
    output_file: str = None,
    output_dir: str = None
):
    """
    🔗 HERB 데이터와 SwissADME 데이터 병합

    Args:
        herb_data_file (str): HERB 성분 JSON 파일 경로
        swissadme_file (str): SwissADME JSON 파일 경로
        output_file (str): 출력 JSON 파일명 (기본: 자동 생성)
        output_dir (str): 출력 디렉토리 (기본: herb_data_file 경로)
    """
    logger.info(f"🚀 데이터 병합 시작: {herb_data_file} + {swissadme_file}")

    herb_data = load_from_json(herb_data_file)
    swissadme_data = load_from_json(swissadme_file)

    if not herb_data or not swissadme_data:
        logger.error("❌ 입력 데이터 중 하나가 비어있습니다.")
        return

    merged = []
    for herb in herb_data:
        match = next(
            (s for s in swissadme_data if s.get("ingredient") == herb.get("ingredient")), None
        )
        if match:
            merged.append({**herb, **match})

    base_name = f"merged_{os.path.splitext(os.path.basename(herb_data_file))[0]}"
    output_dir = output_dir or os.path.dirname(herb_data_file)
    os.makedirs(output_dir, exist_ok=True)
    output_file = output_file or f"{base_name}.json"
    output_path = os.path.join(output_dir, output_file)

    save_to_json(merged, output_path)
    logger.info(f"✅ 병합 완료: {len(merged)}개 항목 → {output_path}")
