import os
import json
import pandas as pd
from modules.data_utils import load_from_json, save_to_json

# 여러 개의 약재 설정
herb_names = ["고삼", "지모", "지황", "치자", "황금", "황련", "황백"]

# 저장 디렉토리 설정
PROCESSED_DIR = "processed"

# 디렉토리 생성
os.makedirs(os.path.join("data", PROCESSED_DIR), exist_ok=True)

def merge_herb_data(herb_name):
    """HERB, SwissADME, BATMAN-TCM 데이터를 개별 약재별로 통합 (JSON 저장)"""
    
    # JSON 파일 불러오기
    batman_filename = f"batman_tcm_results_{herb_name}.json"
    swissadme_filename = f"swissadme_processed_results_{herb_name}.json"

    batman_data = load_from_json(batman_filename, subdir="raw")
    swissadme_data = load_from_json(swissadme_filename, subdir=PROCESSED_DIR)  # ✅ 수정: SwissADME 파일을 "raw"에서 가져오도록

    if not batman_data:
        print(f"⚠️ BATMAN-TCM 데이터 없음: {batman_filename}")
        return []
    
    # SwissADME 데이터 없을 경우 빈 리스트로 처리
    if not swissadme_data:
        print(f"⚠️ SwissADME 데이터 없음: {swissadme_filename}")
        swissadme_data = []

    # ✅ SwissADME 데이터를 딕셔너리로 변환 (ingredient_name 기준) + 내부 `swissadme_results`까지 포함
    swissadme_dict = {}
    for item in swissadme_data:
        ingredient_name = item.get("ingredient_name", "")
        swissadme_info = item.get("swissadme_results", {})  # ✅ `swissadme_results` 내부 정보 추출

        # ✅ `swissadme_results` 내부의 모든 키를 가져와 저장
        swissadme_dict[ingredient_name] = {
            "molecule_smile": item.get("molecule_smile", ""),
            **swissadme_info  # ✅ 내부의 모든 SwissADME 정보를 병합
        }

    merged_results = []
    
    # BATMAN-TCM 데이터 병합
    for item in batman_data:
        ingredient_name = item.get("ingredient_name", "")
        ingredient_url = item.get("ingredient_url", "")
        pubchem_id = item.get("PubChem id", "")

        # ✅ SwissADME 정보 가져오기 (없을 경우 빈 값 처리)
        swissadme_info = swissadme_dict.get(ingredient_name, {})

        # BATMAN-TCM 타겟 정보 가져오기
        batman_results = item.get("batman_tcm_results", {})

        # `batman_tcm_results`가 `dict`인지 확인 후 `target` 리스트 가져오기
        targets = batman_results.get("target", []) if isinstance(batman_results, dict) else []

        # 데이터 병합
        merged_entry = {
            "Herb": herb_name,
            "Ingredient Name": ingredient_name,
            "Ingredient URL": ingredient_url,
            "PubChem ID": pubchem_id,
            **swissadme_info,  # ✅ SwissADME 정보 추가 (모든 키 포함)
            "Targets": targets  # 타겟 유전자 정보 리스트 그대로 유지
        }
        
        merged_results.append(merged_entry)

    # 개별 JSON 파일 저장
    output_json_file = f"merged_results_{herb_name}.json"
    save_to_json(merged_results, output_json_file, subdir="processed")

    print(f"✅ 병합 완료: {output_json_file}")

    return merged_results


def merge_data():
    """모든 약재 데이터를 통합하여 하나의 JSON 파일로 저장"""
    all_data = {}

    for herb in herb_names:
        merged_results = merge_herb_data(herb)
        if merged_results:
            all_data[herb] = merged_results

    # 전체 JSON 저장
    output_json_file = "final_merged_results.json"
    save_to_json(all_data, output_json_file, subdir=PROCESSED_DIR)

    print(f"✅ 전체 병합 완료: {output_json_file}")
