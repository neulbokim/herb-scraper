import os
import json
import requests
import time
import pandas as pd
from modules.data_utils import save_to_json, load_from_json
from modules.string_api import get_compound_targets

# ✅ 데이터 경로 설정
STRING_DATA_DIR = "data/string"
PROCESSED_DATA_DIR = "data/processed"

# ✅ 디렉토리 생성
os.makedirs(STRING_DATA_DIR, exist_ok=True)

# ✅ 대상 약재 리스트
herbs_list = ["고삼", "마황", "오미자", "인삼", "지모", "지황", "치자", "황금", "황련", "황백"]

def load_compounds(herb_name):
    """📂 특정 약재의 JSON 파일에서 성분 목록 가져오기"""
    file_path = os.path.join(PROCESSED_DATA_DIR, f"swissadme_processed_results_{herb_name}.json")

    if not os.path.exists(file_path):
        print(f"⚠️ 파일 없음: {file_path}")
        return []

    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    return data


def process_herb(herb_name):
    """🔹 특정 약재의 성분을 가져와 STRING API로 타겟 단백질 조회"""
    print(f"\n🔹 '{herb_name}'의 성분 데이터 로드 중...")
    compounds = load_compounds(herb_name)

    if not compounds:
        print(f"⚠️ '{herb_name}'의 유효한 성분 데이터가 없습니다. 스킵합니다.")
        return

    print(f"\n🔹 STRING API에서 '{herb_name}'의 성분 {len(compounds)}개에 대한 타겟 단백질 조회 중...")
    compound_targets = get_compound_targets(compounds)

    # 🔹 약재 정보 추가
    for entry in compound_targets:
        entry["Herb"] = herb_name

    # 🔹 JSON 및 CSV 저장
    output_json = os.path.join(STRING_DATA_DIR, f"compound_targets_{herb_name}.json")
    output_csv = os.path.join(STRING_DATA_DIR, f"compound_targets_{herb_name}.csv")

    save_to_json(compound_targets, f"compound_targets_{herb_name}.json", subdir="string")

    df = pd.DataFrame(compound_targets)
    df.to_csv(output_csv, index=False)

    print(f"✅ '{herb_name}'의 타겟 단백질 데이터 저장 완료!")
    print(f"   📂 JSON: {output_json}")
    print(f"   📂 CSV: {output_csv}")


if __name__ == "__main__":
    print("🔹 실행 가능한 약재 목록:", herbs_list)
    selected_herb = input("🌿 특정 약재를 입력하세요 (전체 실행: enter): ").strip()

    if selected_herb:
        if selected_herb in herbs_list:
            process_herb(selected_herb)
        else:
            print(f"⚠️ '{selected_herb}'는 유효한 약재명이 아닙니다. 실행 가능한 목록을 확인하세요: {herbs_list}")
    else:
        print("\n🔹 전체 약재에 대해 실행합니다...")
        for herb in herbs_list:
            process_herb(herb)

    print("\n✅ 모든 작업 완료!")