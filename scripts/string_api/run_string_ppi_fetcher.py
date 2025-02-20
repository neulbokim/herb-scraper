# scripts/string_api/run_string_ppi_fetcher.py

from modules.string_api.string_ppi_fetcher import fetch_ppi_data
from modules.utils import load_from_json, save_to_json, setup_logger
import argparse
import os

logger = setup_logger("run_string_ppi_fetcher")


def main():
    parser = argparse.ArgumentParser(description="🔗 STRING PPI 데이터 수집 실행")
    parser.add_argument("input_file", type=str, help="입력 JSON 파일 경로 (STRING ID 목록 필요)")
    parser.add_argument(
        "-o", "--output_file", type=str, help="출력 JSON 파일 경로 (기본: string_ppi_results.json)", default="string_ppi_results.json"
    )
    parser.add_argument(
        "-s", "--species", type=int, help="종(species) 코드 (기본: 9606)", default=9606
    )

    args = parser.parse_args()

    input_file = args.input_file
    output_file = args.output_file
    species = args.species

    logger.info(f"🚀 STRING PPI 데이터 수집 시작: {input_file}")

    string_ids_data = load_from_json(input_file)
    if not string_ids_data:
        logger.error(f"❌ 입력 파일 오류: STRING ID 데이터 없음 → {input_file}")
        return

    string_ids = [entry.get("string_id") for entry in string_ids_data if entry.get("string_id")]
    if not string_ids:
        logger.error("❌ 유효한 STRING ID 없음")
        return

    ppi_results = fetch_ppi_data(string_ids, species=species)
    save_to_json(ppi_results, output_file)

    logger.info(f"✅ PPI 데이터 수집 완료 → {output_file}")


if __name__ == "__main__":
    main()
