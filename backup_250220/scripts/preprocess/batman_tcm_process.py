import os
import pandas as pd
from modules.data_utils import load_from_json, save_to_json

# 여러 개의 약재 설정
herb_names = ["오미자"]

# 처리된 데이터 저장 디렉토리 설정
PROCESSED_DIR = "processed"

# 출력 디렉토리 생성
os.makedirs(os.path.join("data", PROCESSED_DIR), exist_ok=True)

def process_json_to_csv_xlsx(herb_name):
    """JSON 파일을 CSV 및 XLSX로 변환하여 저장"""
    filename = f"batman_tcm_results_{herb_name}.json"
    data = load_from_json(filename, subdir=PROCESSED_DIR)

    if not data:
        print(f"⚠️ 데이터 없음: {filename}")
        return

    rows = []
    for item in data:
        ingredient_url = item.get("ingredient_url", "")
        ingredient_name = item.get("ingredient_name", "")
        pubchem_id = item.get("PubChem id", "")

        batman_results = item.get("batman_tcm_results", {})
        if "target" in batman_results and isinstance(batman_results["target"], list):
            for target in batman_results["target"]:
                rows.append({
                    "Ingredient URL": ingredient_url,
                    "Ingredient Name": ingredient_name,
                    "PubChem ID": pubchem_id,
                    "Gene ID": target.get("gene_id", ""),
                    "Gene Name": target.get("gene_name", ""),
                    "Score": target.get("score", "")
                })
        else:
            rows.append({
                "Ingredient URL": ingredient_url,
                "Ingredient Name": ingredient_name,
                "PubChem ID": pubchem_id,
                "Gene ID": "",
                "Gene Name": "",
                "Score": ""
            })

    # 데이터프레임 생성
    df = pd.DataFrame(rows)

    # 파일 저장 경로 설정
    # output_csv_path = os.path.join("data", PROCESSED_DIR, f"batman_tcm_results_{herb_name}.csv")
    output_xlsx_path = os.path.join("data", PROCESSED_DIR, f"batman_tcm_results_{herb_name}.xlsx")

    # CSV 및 XLSX 저장
    # df.to_csv(output_csv_path, index=False, encoding="utf-8-sig")
    df.to_excel(output_xlsx_path, index=False, engine="openpyxl")

    print(f"✅ 변환 완료: {output_xlsx_path}")

# 모든 약재에 대해 변환 실행
for herb in herb_names:
    process_json_to_csv_xlsx(herb)
