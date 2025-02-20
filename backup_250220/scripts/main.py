import os
from scripts.herb_scraper import main as herb_main
from scripts.swissadme_query import main as swissadme_main
from scripts.swissadme_process import filter_swissadme_data
from scripts.batman_tcm_query import main as batman_main
from scripts.preprocess_data import merge_data

if __name__ == "__main__":
    print("🚀 데이터 수집 파이프라인 실행 시작!")

    # HERB 크롤링
    print("\n🔍 1. HERB 데이터 크롤링 시작...")
    herb_main()

    # SwissADME 크롤링
    print("\n🔍 2. SwissADME 데이터 크롤링 시작...")
    swissadme_main()

    # SwissADME 데이터 필터링
    print("\n🔍 3. SwissADME 데이터 필터링 시작...")
    filter_swissadme_data()

    # BATMAN-TCM API 호출
    print("\n🔍 4. BATMAN-TCM API 데이터 수집 시작...")
    batman_main()

    # 데이터 통합 및 최종 데이터셋 생성
    print("\n🔍 5. 최종 데이터셋 생성 시작...")
    merge_data()

    print("\n✅ 전체 데이터 수집 및 정리 완료! `data/processed/final_dataset.csv` 파일 확인")