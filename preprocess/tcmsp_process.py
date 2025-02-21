# preprocess/tcmsp_process.py

import json
import os
import pandas as pd
from modules.data_utils import save_to_json, save_to_csv
from config.settings import (
    TCMSP_DIR,
    HERB_GROUP_NAME,
    RAW_DATA_PATH,
    PROCESSED_EXCEL_PATH,
    OB_THRESHOLD,
    DL_THRESHOLD
)

def filter_ingredients(ingredients):
    return [ing for ing in ingredients if ing["ob"] >= OB_THRESHOLD and ing["dl"] >= DL_THRESHOLD]

def filter_targets(targets, filtered_ingredients):
    valid_mol_ids = {ing["mol_id"] for ing in filtered_ingredients}
    return [
        {**target, **next((ing for ing in filtered_ingredients if ing["mol_id"] == target["mol_id"]), {})}
        for target in targets if target["mol_id"] in valid_mol_ids
    ]

with open(RAW_DATA_PATH, "r", encoding="utf-8") as f:
    raw_data = json.load(f)

for herb, herb_data in raw_data.items():
    print(f"📌 {herb} 데이터 필터링 중...")
    filtered_ingredients = filter_ingredients(herb_data["ingredients"])
    filtered_targets = filter_targets(herb_data["targets"], filtered_ingredients)

    save_to_json(filtered_ingredients, f"tcmsp_{herb}_filtered_ingredients.json", "tcmsp")
    save_to_csv(filtered_ingredients, f"tcmsp_{herb}_filtered_ingredients.csv", "tcmsp")
    save_to_json(filtered_targets, f"tcmsp_{herb}_filtered_targets.json", "tcmsp")
    save_to_csv(filtered_targets, f"tcmsp_{herb}_filtered_targets.csv", "tcmsp")
    print(f"✅ {herb} 필터링 완료 및 저장!")

with pd.ExcelWriter(PROCESSED_EXCEL_PATH, engine="xlsxwriter") as writer:
    for herb in raw_data.keys():
        csv_path = os.path.join(TCMSP_DIR, f"tcmsp_{herb}_filtered_targets.csv")
        if os.path.exists(csv_path):
            df = pd.read_csv(csv_path)
            df.to_excel(writer, sheet_name=herb[:31], index=False)

print(f"📁 모든 필터링된 타겟 데이터를 {PROCESSED_EXCEL_PATH}에 저장 완료!")
