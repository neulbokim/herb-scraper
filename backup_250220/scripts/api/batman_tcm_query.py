import os
import json
import pandas as pd
from modules.batman_tcm_utils import get_target_proteins
from modules.data_utils import save_to_json

# 파일 경로 설정
CSV_FILE = "data/raw/active_ingredients_pubchemID.csv"
OUTPUT_FILE = "batman_tcm_results.json"

def run_batman_tcm_from_csv():
    """CSV 파일에서 PubChem ID 값을 가져와 BATMAN-TCM 실행"""

    if not os.path.exists(CSV_FILE):
        print(f"❌ CSV 파일이 없습니다: {CSV_FILE}")
        return

    # ✅ CSV 파일 읽기
    df = pd.read_csv(CSV_FILE)

    required_columns = {"약재명", "활성성분", "PubChem ID"}
    if not required_columns.issubset(df.columns):
        print(f"❌ CSV 파일에 필요한 열({required_columns})이 없습니다.")
        return

    ingredient_map = {}  # ✅ PubChem ID를 key로 한약재 정보를 저장
    pubchem_list = []  # ✅ 실제 API 호출할 PubChem ID 리스트

    for _, row in df.iterrows():
        pubchem_id = str(row["PubChem ID"]).strip() if pd.notna(row["PubChem ID"]) else "N/A"

        # ✅ 소수점(".0") 제거
        pubchem_id = pubchem_id.replace(".0", "")

        # ✅ PubChem ID가 있으면 리스트에 추가
        if pubchem_id not in ["", "N/A", "Not Available"]:
            pubchem_list.append(pubchem_id)

        # ✅ PubChem ID가 없어도 결과에 포함되도록 설정
        ingredient_map[pubchem_id] = {
            "herb_name": row["약재명"],
            "ingredient_name": row["활성성분"],
            "PubChem id": pubchem_id,  # ✅ PubChem ID 없으면 "N/A"로 저장
            "batman_tcm_results": []  # ✅ 기본적으로 빈 리스트로 추가
        }

    # ✅ BATMAN-TCM API 호출
    if pubchem_list:
        print(f"🚀 BATMAN-TCM 분석 시작! 총 {len(pubchem_list)} 개의 PubChem ID 처리 중...")
        batman_tcm_results = get_target_proteins(pubchem_list)

        # ✅ API 결과 병합
        for pubchem_id, data in batman_tcm_results.items():
            if pubchem_id in ingredient_map:
                ingredient_map[pubchem_id]["batman_tcm_results"] = data  # ✅ 전체 결과 저장

    # ✅ JSON 파일 저장
    final_results = list(ingredient_map.values())  # ✅ 리스트로 변환하여 저장
    save_to_json(final_results, OUTPUT_FILE)

    print(f"✅ BATMAN-TCM 결과 저장 완료: {OUTPUT_FILE}")

if __name__ == "__main__":
    run_batman_tcm_from_csv()
