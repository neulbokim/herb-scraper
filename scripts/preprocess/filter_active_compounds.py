# scripts/preprocess/filter_active_compounds.py

from modules.preprocessors.filter_compounds import filter_active_compounds
from modules.utils import load_from_json, save_to_json, setup_logger
import argparse
import os

logger = setup_logger("filter_active_compounds")


def main():
    parser = argparse.ArgumentParser(description="🧹 활성 성분 필터링 실행")
    parser.add_argument("input_file", type=str, help="입력 JSON 파일 경로")
    parser.add_argument(
        "-o", "--output_file", type=str, help="출력 JSON 파일 경로 (기본: filtered_<input_file>.json)", default=None
    )
    parser.add_argument(
        "-t", "--tpsa_threshold", type=float, help="TPSA 필터링 기준 (기본: 140)", default=140
    )

    args = parser.parse_args()

    input_file = args.input_file
    output_file = args.output_file or os.path.splitext(input_file)[0] + "_filtered.json"
    tpsa_threshold = args.tpsa_threshold

    logger.info(f"🚀 필터링 시작: {input_file} → {output_file} (TPSA < {tpsa_threshold})")

    data = load_from_json(input_file)
    if not data:
        logger.error(f"❌ 입력 파일 로드 실패: {input_file}")
        return

    filtered_data = filter_active_compounds(data, tpsa_threshold)
    save_to_json(filtered_data, output_file)

    logger.info(f"✅ 필터링 완료: {len(filtered_data)}개 성분")


if __name__ == "__main__":
    main()

