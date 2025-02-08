import os
import json
import pandas as pd
from modules.data_utils import load_from_json

# 입력 및 출력 파일 경로 설정
INPUT_JSON_FILE = "final_merged_results.json"
OUTPUT_XLSX_FILE = "final_merged_results.xlsx"
PROCESSED_DIR = "processed"

# JSON 데이터 불러오기
data = load_from_json(INPUT_JSON_FILE, subdir=PROCESSED_DIR)

# 변환된 데이터를 저장할 리스트
rows = []

# JSON 데이터를 판다스 데이터프레임 형식으로 변환
for herb_name, ingredients in data.items():
    for ingredient in ingredients:
        base_info = {
            "Herb": herb_name,
            "Ingredient Name": ingredient.get("Ingredient Name", ""),
            "Ingredient URL": ingredient.get("Ingredient URL", ""),
            "PubChem ID": ingredient.get("PubChem ID", ""),
            "Molecule SMILES": ingredient.get("molecule_smile", ""),
            "TPSA": ingredient.get("TPSA", ""),
            "GI absorption": ingredient.get("GI absorption", ""),
            "Lipinski": ingredient.get("Lipinski", ""),
            "Bioavailability": ingredient.get("Bioavailability Score", ""),
            "Ghose": ingredient.get("Ghose", ""),  # ✅ 추가된 SwissADME 필드
            "Veber": ingredient.get("Veber", ""),
            "Egan": ingredient.get("Egan", ""),
            "Muegge": ingredient.get("Muegge", ""),
            "Formula": ingredient.get("Formula", ""),
        }

        # 타겟 유전자 정보가 여러 개일 경우, 개별 행으로 변환
        targets = ingredient.get("Targets", [])
        if targets:
            for target in targets:
                row = base_info.copy()
                row["Gene ID"] = target.get("gene_id", "")
                row["Gene Name"] = target.get("gene_name", "")
                row["Score"] = target.get("score", "")
                rows.append(row)
        else:
            # 타겟 정보가 없는 경우 빈 값으로 추가
            row = base_info.copy()
            row["Gene ID"] = ""
            row["Gene Name"] = ""
            row["Score"] = ""
            rows.append(row)

# 데이터프레임 생성
df = pd.DataFrame(rows)

# XLSX 저장
output_xlsx_path = os.path.join("data", PROCESSED_DIR, OUTPUT_XLSX_FILE)
df.to_excel(output_xlsx_path, index=False, engine="openpyxl")

print(f"✅ 변환 완료: {output_xlsx_path}")
