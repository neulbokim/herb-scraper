# scripts/converters/convert_to_xlsx.py

from modules.converters.to_xlsx import convert_json_to_xlsx
from modules.utils import setup_logger
import argparse
import os

logger = setup_logger("convert_to_xlsx")


def main():
    parser = argparse.ArgumentParser(description="🔄 JSON → XLSX 변환")
    parser.add_argument("input_file", type=str, help="입력 JSON 파일 경로")
    parser.add_argument("-o", "--output_file", type=str, help="출력 XLSX 파일 경로", default=None)
    args = parser.parse_args()

    input_file = args.input_file
    output_file = args.output_file or os.path.splitext(input_file)[0] + ".xlsx"

    logger.info(f"🚀 변환 시작: {input_file} → {output_file}")
    convert_json_to_xlsx(input_file, output_file)
    logger.info("✅ 변환 완료")


if __name__ == "__main__":
    main()
