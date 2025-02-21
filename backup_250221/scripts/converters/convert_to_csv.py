# scripts/converters/convert_to_csv.py

from modules.converters.to_csv import convert_json_to_csv
from modules.utils import setup_logger
import argparse
import os

logger = setup_logger("convert_to_csv")


def main():
    parser = argparse.ArgumentParser(description="🔄 JSON → CSV 변환")
    parser.add_argument("input_file", type=str, help="입력 JSON 파일 경로")
    parser.add_argument("-o", "--output_file", type=str, help="출력 CSV 파일 경로", default=None)
    args = parser.parse_args()

    input_file = args.input_file
    output_file = args.output_file or f"{os.path.splitext(input_file)[0]}.csv"

    logger.info(f"🚀 변환 시작: {input_file} → {output_file}")
    convert_json_to_csv(input_file, output_file)
    logger.info("✅ 변환 완료")


if __name__ == "__main__":
    main()
