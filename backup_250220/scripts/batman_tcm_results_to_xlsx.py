import os
import pandas as pd
from modules.data_utils import load_from_json

# 🔹 파일 경로 설정
INPUT_JSON_FILE = "batman_tcm_results_인삼.json"
OUTPUT_XLSX_FILE = "batman_tcm_results_인삼.xlsx"
PROCESSED_DIR = "processed"

def convert_batman_results_to_xlsx():
    """BATMAN-TCM 결과 JSON을 XLSX로 변환"""

    # ✅ JSON 파일 불러오기
    data = load_from_json(INPUT_JSON_FILE, subdir=PROCESSED_DIR)

    if not data:
        print(f"❌ JSON 파일이 비어 있거나 존재하지 않습니다: {INPUT_JSON_FILE}")
        return

    expanded_rows = []

    # 🔹 데이터 변환 (성분 정보 + 타겟 단백질 정보를 모두 포함)
    for compound in data:
        herb_name = compound.get("Herb", "Unknown")
        ingredient_name = compound.get("Ingredient Name", "Unknown")
        ingredient_url = compound.get("Ingredient URL", "")
        pubchem_id = compound.get("PubChem ID", "N/A")

        # ✅ BATMAN-TCM 분석 결과 가져오기 (리스트 or 딕셔너리)
        batman_tcm_results = compound.get("batman_tcm_results", [])

        if isinstance(batman_tcm_results, list):
            if len(batman_tcm_results) > 0:
                batman_results = batman_tcm_results[0]  # 첫 번째 요소 선택
            else:
                batman_results = {}  # 빈 리스트인 경우 빈 딕셔너리로 처리
        elif isinstance(batman_tcm_results, dict):
            batman_results = batman_tcm_results  # 이미 딕셔너리라면 그대로 사용
        else:
            batman_results = {}  # 다른 경우도 빈 딕셔너리 처리

        # ✅ "target" 리스트 가져오기
        targets = batman_results.get("target", [])

        if isinstance(targets, list) and len(targets) > 0:
            for target in targets:
                expanded_rows.append({
                    "Herb": herb_name,
                    "Ingredient Name": ingredient_name,
                    "Ingredient URL": ingredient_url,
                    "PubChem ID": pubchem_id,
                    "BATMAN-TCM Name": batman_results.get("name", ""),
                    "BATMAN-TCM CID": batman_results.get("cid", ""),
                    "Gene ID": target.get("gene_id", ""),
                    "Gene Name": target.get("gene_name", ""),
                    "Score": target.get("score", "")
                })
        else:
            # 🔹 타겟 정보가 없는 경우에도 성분 정보만 저장
            expanded_rows.append({
                "Herb": herb_name,
                "Ingredient Name": ingredient_name,
                "Ingredient URL": ingredient_url,
                "PubChem ID": pubchem_id,
                "BATMAN-TCM Name": batman_results.get("name", ""),
                "BATMAN-TCM CID": batman_results.get("cid", ""),
                "Gene ID": "",
                "Gene Name": "",
                "Score": ""
            })

    # 🔹 DataFrame 생성
    df = pd.DataFrame(expanded_rows)

    # 🔹 엑셀 파일 저장
    output_xlsx_path = os.path.join("data", PROCESSED_DIR, OUTPUT_XLSX_FILE)
    df.to_excel(output_xlsx_path, index=False, engine="openpyxl")

    print(f"✅ BATMAN-TCM 결과를 XLSX로 저장 완료: {output_xlsx_path}")

if __name__ == "__main__":
    convert_batman_results_to_xlsx()
