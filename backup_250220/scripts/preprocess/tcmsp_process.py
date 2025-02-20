import json
import os
import pandas as pd
from modules.data_utils import save_to_json, save_to_csv

# ✅ 설정
TCMSP_DIR = "data/tcmsp"
HERB_GROUP_NAME = "고삼자초지모"
HERBS = ["고삼", "자초", "지모"]
OB_THRESHOLD = 30
DL_THRESHOLD = 0.18

# ✅ 필터링 함수
def filter_ingredients(ingredients):
    return [ing for ing in ingredients if ing["ob"] >= OB_THRESHOLD and ing["dl"] >= DL_THRESHOLD]

def filter_targets(targets, filtered_ingredients):
    valid_mol_ids = {ing["mol_id"] for ing in filtered_ingredients}
    return [
        {**target, **next((ing for ing in filtered_ingredients if ing["mol_id"] == target["mol_id"]), {})}
        for target in targets if target["mol_id"] in valid_mol_ids
    ]

# ✅ 전체 raw 데이터 로드
raw_data_path = os.path.join(TCMSP_DIR, f"tcmsp_raw_results_{HERB_GROUP_NAME}.json")

with open(raw_data_path, "r", encoding="utf-8") as f:
    raw_data = json.load(f)

# ✅ 필터링 및 저장
for herb in HERBS:
    print(f"📌 {herb} 데이터 필터링 중...")

    raw_ingredients = raw_data[herb]["ingredients"]
    raw_targets = raw_data[herb]["targets"]

    filtered_ingredients = filter_ingredients(raw_ingredients)
    filtered_targets = filter_targets(raw_targets, filtered_ingredients)

    # ✅ 필터링된 데이터 저장
    save_to_json(filtered_ingredients, f"tcmsp_{herb}_filtered_ingredients.json", "tcmsp")
    save_to_csv(filtered_ingredients, f"tcmsp_{herb}_filtered_ingredients.csv", "tcmsp")
    save_to_json(filtered_targets, f"tcmsp_{herb}_filtered_targets.json", "tcmsp")
    save_to_csv(filtered_targets, f"tcmsp_{herb}_filtered_targets.csv", "tcmsp")

    print(f"✅ {herb} 필터링 완료 및 저장!")

# ✅ 엑셀 시트 통합 저장
excel_path = os.path.join(TCMSP_DIR, f"tcmsp_filtered_targets_{HERB_GROUP_NAME}.xlsx")

with pd.ExcelWriter(excel_path, engine="xlsxwriter") as writer:
    for herb in HERBS:
        csv_path = os.path.join(TCMSP_DIR, f"tcmsp_{herb}_filtered_targets.csv")
        if os.path.exists(csv_path):
            df = pd.read_csv(csv_path)
            df.to_excel(writer, sheet_name=herb, index=False)

print(f"📁 모든 필터링된 타겟 데이터를 {excel_path}에 저장 완료!")
