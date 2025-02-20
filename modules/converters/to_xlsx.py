# modules/converters/to_xlsx.py

import pandas as pd
from modules.utils import load_from_json, save_to_excel, setup_logger
import os

logger = setup_logger("to_xlsx")

def convert_to_xlsx(input_file: str, output_file: str = None, output_dir: str = None):
    """
    🔄 JSON 파일을 XLSX 파일로 변환

    Args:
        input_file (str): 입력 JSON 파일 경로
        output_file (str): 출력 XLSX 파일명 (기본: 입력 파일명 기반)
        output_dir (str): 출력 디렉토리 경로 (기본: 입력 파일과 동일한 디렉토리)
    """
    logger.info(f"🚀 JSON → XLSX 변환 시작: {input_file}")

    data = load_from_json(input_file)
    if not data:
        logger.error(f"❌ 입력 JSON 파일이 비어있거나 잘못되었습니다: {input_file}")
        return

    df = pd.DataFrame(data)
    base_name = os.path.splitext(os.path.basename(input_file))[0]
    output_dir = output_dir or os.path.dirname(input_file)
    os.makedirs(output_dir, exist_ok=True)
    output_file = output_file or f"{base_name}.xlsx"
    output_path = os.path.join(output_dir, output_file)

    save_to_excel(df, output_path)
    logger.info(f"✅ 변환 완료 → {output_path}")
