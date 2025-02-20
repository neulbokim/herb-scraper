# scripts/string_api/run_string_id_fetcher.py

from modules.string_api.string_id_fetcher import fetch_string_ids
from modules.utils import load_csv, save_to_json, setup_logger
import argparse
import os

logger = setup_logger("run_string_id_fetcher")


def main():
    parser = argparse.ArgumentParser(description="🆔 STRING ID 조회 실행")
    parser.add_argument("input_file", type=str, help="입력 CSV 파일 경로 (Gene Name 열 필요)")
    parser.add_argument(
        "-o", "--output_file", type=str, help="출력 JSON 파일 경로 (기본: string_id_map.json)", default="string_id_map.json"
    )
    parser.add_argument(
        "-s", "--species", type=int, help="종(species) 코드 (기본: 9606)", default=9606
    )

    args = parser.parse_args()

    input_file = args.input_file
    output_file = args.output_file
    species = args.species

    logger.info(f"🚀 STRING ID 조회 시작: {input_file}")

    gene_data = load_csv(input_file)
    if gene_data.empty or "Gene Name" not in gene_data.columns:
        logger.error(f"❌ 입력 파일 오류: Gene Name 열이 없거나 파일이 비어있음 → {input_file}")
        return

    string_ids = fetch_string_ids(gene_data["Gene Name"].tolist(), species=species)
    save_to_json(string_ids, output_file)

    logger.info(f"✅ STRING ID 조회 완료 → {output_file}")


if __name__ == "__main__":
    main()

