# scripts/string_api/run_compound_target_fetcher.py

from modules.string_api.compound_target_fetcher import fetch_compound_targets
from modules.utils import load_from_json, save_to_json, setup_logger
import argparse
import os

logger = setup_logger("run_compound_target_fetcher")


def main():
    parser = argparse.ArgumentParser(description="🎯 화합물-타겟 단백질 매핑 실행")
    parser.add_argument("input_file", type=str, help="입력 JSON 파일 경로 (화합물 목록 필요)")
    parser.add_argument(
        "-o", "--output_file", type=str, help="출력 JSON 파일 경로 (기본: compound_targets.json)", default="compound_targets.json"
    )
    parser.add_argument(
        "-s", "--species", type=int, help="종(species) 코드 (기본: 9606)", default=9606
    )

    args = parser.parse_args()

    input_file = args.input_file
    output_file = args.output_file
    species = args.species

    logger.info(f"🚀 화합물-타겟 매핑 시작: {input_file}")

    compounds_data = load_from_json(input_file)
    if not compounds_data:
        logger.error(f"❌ 입력 파일 오류: 화합물 데이터 없음 → {input_file}")
        return

    compounds = [entry.get("compound") for entry in compounds_data if entry.get("compound")]
    if not compounds:
        logger.error("❌ 유효한 화합물 없음")
        return

    target_mappings = fetch_compound_targets(compounds, species=species)
    save_to_json(target_mappings, output_file)

    logger.info(f"✅ 화합물-타겟 매핑 완료 → {output_file}")


if __name__ == "__main__":
    main()

