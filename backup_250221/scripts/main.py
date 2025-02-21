# scripts/main.py

import argparse
import time
from scripts.crawlers import crawl_tcmsp
from scripts.converters import (
    convert_json_to_csv,
    convert_json_to_xlsx,
    convert_csv_to_json
)
from modules.utils import setup_logger

logger = setup_logger("main_pipeline")


def run_step(step_name, function, *args, **kwargs):
    """🚦 공통 단계 실행 함수"""
    logger.info(f"🚀 [{step_name}] 시작")
    start_time = time.time()

    try:
        function(*args, **kwargs)
        elapsed = time.time() - start_time
        logger.info(f"✅ [{step_name}] 완료 (⏱️ {elapsed:.2f}s)")
    except Exception as e:
        logger.error(f"❌ [{step_name}] 실패: {e}")


def run_pipeline(args):
    """🌱 전체 파이프라인 실행"""

    if args.crawl:
        run_step("TCMSP 크롤링", crawl_tcmsp)

    if args.convert:
        run_step("JSON → CSV 변환", convert_json_to_csv)
        run_step("JSON → XLSX 변환", convert_json_to_xlsx)
        run_step("CSV → JSON 변환", convert_csv_to_json)

    logger.info("🎉 전체 파이프라인 완료")


def main():
    parser = argparse.ArgumentParser(description="🌿 TCMSP 크롤링 및 데이터 변환 파이프라인 실행")
    parser.add_argument(
        "--crawl", action="store_true", help="🕷️ TCMSP 크롤링 단계 실행"
    )
    parser.add_argument(
        "--convert", action="store_true", help="🔄 데이터 변환 단계 실행"
    )

    args = parser.parse_args()

    if not (args.crawl or args.convert):
        logger.warning("⚠️ 실행할 단계를 선택하세요: --crawl, --convert")
        return

    run_pipeline(args)


if __name__ == "__main__":
    main()
