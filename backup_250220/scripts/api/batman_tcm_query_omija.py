import os
import json
import pandas as pd
from modules.batman_tcm_utils import get_target_proteins
from modules.data_utils import load_from_json, save_to_json

# 🔹 파일 경로 설정
INPUT_JSON_FILE = "filtered_active_compounds.json"
OUTPUT_JSON_FILE = "batman_tcm_results_인삼.json"

def run_batman_tcm_for_omija():
    """filtered_active_compounds.json에서 오미자 데이터를 가져와 BATMAN-TCM 실행"""

    # ✅ JSON 파일 불러오기
    data = load_from_json(INPUT_JSON_FILE, subdir="processed")

    if not data or "인삼" not in data:
        print(f"❌ JSON 파일이 비어 있거나 '인삼' 데이터가 없습니다: {INPUT_JSON_FILE}")
        return

    # ✅ 오미자 데이터 가져오기
    omija_data = data["인삼"]

    if not omija_data:
        print("⚠️ 인삼 데이터가 없습니다.")
        return

    ingredient_map = {}  # ✅ PubChem ID를 key로 한약재 정보를 저장
    pubchem_list = []  # ✅ API 호출할 PubChem ID 리스트

    for compound in omija_data:
        pubchem_id = str(compound.get("PubChem ID", "N/A")).strip()

        # ✅ 소수점(".0") 제거
        pubchem_id = pubchem_id.replace(".0", "")

        # ✅ 기본 데이터 구조 설정
        ingredient_map[pubchem_id] = {
            "Herb": "인삼",
            "Ingredient Name": compound.get("Ingredient Name", "Unknown"),
            "Ingredient URL": compound.get("Ingredient URL", ""),
            "PubChem ID": pubchem_id if pubchem_id not in ["", "N/A", "Not Available"] else "N/A",
            "batman_tcm_results": []  # ✅ 기본적으로 빈 리스트로 추가
        }

        # ✅ PubChem ID가 유효하면 API 요청 리스트에 추가
        if pubchem_id not in ["", "N/A", "Not Available"]:
            pubchem_list.append(pubchem_id)

    # ✅ 디버깅용 출력: API 요청 리스트 확인
    print(f"🚀 API 요청할 PubChem ID 목록: {pubchem_list}")

    # ✅ BATMAN-TCM API 호출 (PubChem ID가 존재하는 경우만)
    if pubchem_list:
        print(f"🚀 BATMAN-TCM 분석 시작! 총 {len(pubchem_list)} 개의 PubChem ID 처리 중...")
        batman_tcm_results = get_target_proteins(pubchem_list)

        # ✅ API 결과 병합
        for pubchem_id, data in batman_tcm_results.items():
            if pubchem_id in ingredient_map:
                ingredient_map[pubchem_id]["batman_tcm_results"] = data  # ✅ API 결과 저장

    # ✅ JSON 파일 저장
    final_results = list(ingredient_map.values())  # ✅ 리스트로 변환하여 저장
    save_to_json(final_results, OUTPUT_JSON_FILE, subdir="processed")

    print(f"✅ BATMAN-TCM 결과 저장 완료: {OUTPUT_JSON_FILE}")

if __name__ == "__main__":
    run_batman_tcm_for_omija()
