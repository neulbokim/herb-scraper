# scripts/preprocess/merge_herb_data.py

from modules.preprocessors.merge_herb_data import merge_herb_data
from modules.utils import load_from_json, save_to_json, setup_logger
import argparse
import os

logger = setup_logger("merge_herb_data")


def main():
    parser = argparse.ArgumentParser(description="🔗 데이터 병합 실행")
    parser.add_argument("input_files", nargs="+", help="병합할 JSON 파일 경로 목록")
    parser.add_argument(
        "-o", "--output_file", type=str, help="출력 JSON 파일 경로 (기본: merged_results.json)", default="merged_results.json"
    )

    args = parser.parse_args()

    input_files = args.input_files
    output_file = args.output_file

    logger.info(f"🚀 데이터 병합 시작: {len(input_files)}개 파일")

    data_list = []
    for file_path in input_files:
        data = load_from_json(file_path)
        if data:
            data_list.append(data)
            logger.info(f"✅ 로드 성공: {file_path}")
        else:
            logger.warning(f"⚠️ 로드 실패: {file_path}")

    if not data_list:
        logger.error("❌ 병합할 데이터 없음")
        return

    merged_data = merge_herb_data(data_list)
    save_to_json(merged_data, output_file)

    logger.info(f"✅ 병합 완료 → {output_file} | 총 {len(merged_data)}개 항목")


if __name__ == "__main__":
    main()
