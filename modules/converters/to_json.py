# modules/converters/to_json.py

import pandas as pd
from modules.utils import save_to_json, setup_logger
import os

logger = setup_logger("to_json")

def convert_to_json(input_file: str, output_file: str = None, output_dir: str = None):
    """
    🔄 CSV 또는 XLSX 파일을 JSON 파일로 변환

    Args:
        input_file (str): 입력 CSV 또는 XLSX 파일 경로
        output_file (str): 출력 JSON 파일명 (기본: 입력 파일명 기반)
        output_dir (str): 출력 디렉토리 경로 (기본: 입력 파일과 동일한 디렉토리)
    """
    logger.info(f"🚀 CSV/XLSX → JSON 변환 시작: {input_file}")

    # 파일 형식 검증
    extension = os.path.splitext(input_file)[1].lower()
    if extension not in [".csv", ".xlsx"]:
        logger.error(f"❌ 지원하지 않는 파일 형식: {extension}")
        return

    try:
        df = pd.read_csv(input_file) if extension == ".csv" else pd.read_excel(input_file)
    except Exception as e:
        logger.error(f"❌ 파일 읽기 실패: {e}")
        return

    data = df.to_dict(orient="records")
    base_name = os.path.splitext(os.path.basename(input_file))[0]
    output_dir = output_dir or os.path.dirname(input_file)
    os.makedirs(output_dir, exist_ok=True)
    output_file = output_file or f"{base_name}.json"
    output_path = os.path.join(output_dir, output_file)

    save_to_json(data, output_path)
    logger.info(f"✅ 변환 완료 → {output_path}")
