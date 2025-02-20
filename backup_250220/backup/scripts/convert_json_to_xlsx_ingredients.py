import os
import pandas as pd
from modules.data_utils import load_from_json

# 경로 설정
INPUT_DIR = "data/raw"
OUTPUT_DIR = "data/raw"

# 변환할 약재 목록
TARGET_HERBS = ["고삼", "지황", "황련", "황백", "지모", "자초", "치자", "황금"]

def convert_selected_herbs_to_xlsx(input_dir, output_dir, target_herbs):
    for herb_name in target_herbs:
        json_file = f"herb_ingredients_{herb_name}.json"
        json_path = os.path.join(input_dir, json_file)

        if not os.path.exists(json_path):
            print(f"⚠️ {herb_name}의 JSON 파일이 존재하지 않습니다. 건너뜀.")
            continue

        print(f"🌿 {herb_name} 변환 시작...")

        # JSON 데이터 로드
        data = load_from_json(json_file, subdir=input_dir.split("/")[-1])

        rows = []
        for url, ingredient_info in data.items():
            row = {
                "Herb": herb_name,
                "Ingredient Name": ingredient_info.get("ingredient_name", ""),
                "Ingredient URL": url,
                "Molecule SMILES": ingredient_info.get("molecule_smile", ""),
                "OB score": ingredient_info.get("OB score", ""),
                "SymMap ID": ingredient_info.get("SymMap id", ""),
                "PubChem ID": ingredient_info.get("PubChem id", ""),
                "TCMID ID": ingredient_info.get("TCMID id", ""),
                "TCMSP ID": ingredient_info.get("TCMSP id", "")
            }
            rows.append(row)

        if not rows:
            print(f"⚠️ {herb_name}에 유효한 데이터가 없습니다. 건너뜀.")
            continue

        # DataFrame 생성 및 XLSX 저장
        df = pd.DataFrame(rows)
        output_file = f"herb_ingredients_{herb_name}.xlsx"
        output_path = os.path.join(output_dir, output_file)
        df.to_excel(output_path, index=False, engine="openpyxl")

        print(f"✅ {herb_name} 데이터 저장 완료: {output_path}")

if __name__ == "__main__":
    convert_selected_herbs_to_xlsx(INPUT_DIR, OUTPUT_DIR, TARGET_HERBS)
