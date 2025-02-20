import os
import json
import pandas as pd
import re
from modules.data_utils import load_from_json, save_to_json

# 🔹 필터링 기준 설정
TPSA_THRESHOLD = 140
BIOAVAILABILITY_THRESHOLD = 0.55
LIPINSKI_MAX_VIOLATION = 1
REQUIRED_DRUGLIKENESS_YES = 4  # ✅ 더 강화된 기준 (최소 4개 이상 Yes 필요)

# 🔹 입력 및 출력 설정
PROCESSED_DIR = "processed"
OUTPUT_JSON_FILE = "filtered_active_compounds_인삼오미자.json"
OUTPUT_XLSX_FILE = "filtered_active_compounds_인삼오미자.xlsx"
HERB_NAMES = ["인삼", "오미자"]

# 🔹 숫자 변환 함수 (TPSA 등)
def clean_float(value, default=0.0):
    """문자열에서 숫자 부분만 추출하여 float 변환 (단위 제거)"""
    try:
        return float(re.sub(r"[^\d.]", "", str(value)))  # 숫자와 점(.)을 제외한 문자 제거 후 변환
    except ValueError:
        return default  # 변환 실패 시 기본값 반환

# 🔹 모든 데이터를 병합할 딕셔너리
merged_filtered_data = {}
xlsx_sheets = {}  # 엑셀 파일에 저장할 데이터 딕셔너리

# 🔹 JSON 데이터 로드 및 필터링
for herb_name in HERB_NAMES:
    input_filename = f"swissadme_processed_results_{herb_name}.json"
    data = load_from_json(input_filename, subdir=PROCESSED_DIR)

    if not data:
        print(f"⚠️ {herb_name}: 파일 {input_filename} 이(가) 비어 있거나 존재하지 않습니다.")
        continue

    filtered_data = []

    for compound in data:
        try:
            # 🔹 필터링 기준 적용
            tpsa = clean_float(compound.get("swissadme_results", {}).get("TPSA", 0))
            gi_absorption = compound.get("swissadme_results", {}).get("GI absorption", "") == "High"
            bioavailability = clean_float(compound.get("swissadme_results", {}).get("Bioavailability Score", 0))
            lipinski = compound.get("swissadme_results", {}).get("Lipinski", "").startswith("Yes") and compound.get("swissadme_results", {}).get("Lipinski", "").count("violation") <= LIPINSKI_MAX_VIOLATION

            # ✅ Druglikeness 조건 강화 (최소 4개 Yes 필요)
            druglikeness_yes_count = sum([
                compound.get("swissadme_results", {}).get("Ghose", "") == "Yes",
                compound.get("swissadme_results", {}).get("Veber", "") == "Yes",
                compound.get("swissadme_results", {}).get("Egan", "") == "Yes",
                compound.get("swissadme_results", {}).get("Muegge", "") == "Yes"
            ])
            druglikeness_pass = lipinski and druglikeness_yes_count >= REQUIRED_DRUGLIKENESS_YES
            pains_alert = compound.get("swissadme_results", {}).get("PAINS", "") == "0 alert"

            # 🔹 최종 필터링 적용
            if tpsa < TPSA_THRESHOLD and gi_absorption and druglikeness_pass and bioavailability >= BIOAVAILABILITY_THRESHOLD and pains_alert:
                filtered_data.append({
                    "Herb": herb_name,
                    "Ingredient Name": compound.get("ingredient_name", ""),
                    "Ingredient URL": compound.get("ingredient_url", ""),
                    "PubChem ID": compound.get("PubChem id", "N/A"),
                    "molecule_smile": compound.get("molecule_smile", ""),
                    "SMILES": compound.get("swissadme_results", {}).get("SMILES", ""),
                    "Formula": compound.get("swissadme_results", {}).get("Formula", ""),
                    "TPSA": compound.get("swissadme_results", {}).get("TPSA", ""),
                    "GI absorption": compound.get("swissadme_results", {}).get("GI absorption", ""),
                    "Lipinski": compound.get("swissadme_results", {}).get("Lipinski", ""),
                    "Ghose": compound.get("swissadme_results", {}).get("Ghose", ""),
                    "Veber": compound.get("swissadme_results", {}).get("Veber", ""),
                    "Egan": compound.get("swissadme_results", {}).get("Egan", ""),
                    "Muegge": compound.get("swissadme_results", {}).get("Muegge", ""),
                    "Bioavailability Score": compound.get("swissadme_results", {}).get("Bioavailability Score", ""),
                    "PAINS": compound.get("swissadme_results", {}).get("PAINS", ""),
                    "Targets": []  # BATMAN-TCM 결과 저장을 위한 빈 리스트
                })

        except Exception as e:
            print(f"⚠️ {herb_name}: 데이터 필터링 중 오류 발생: {e}")

    # ✅ 병합 리스트에 추가
    if filtered_data:
        merged_filtered_data[herb_name] = filtered_data

    # ✅ 엑셀 저장을 위한 시트 데이터 저장
    df = pd.json_normalize(filtered_data, sep="_")
    xlsx_sheets[herb_name] = df  # 엑셀 파일에서 각 약재별 시트로 저장할 데이터

# 🔹 필터링된 데이터를 JSON으로 저장
output_json_path = os.path.join("data", PROCESSED_DIR, OUTPUT_JSON_FILE)
save_to_json(merged_filtered_data, OUTPUT_JSON_FILE, subdir=PROCESSED_DIR)
print(f"📁 JSON 저장 완료: {output_json_path}")

# 🔹 필터링된 데이터를 엑셀에 약재별 시트로 저장
output_xlsx_path = os.path.join("data", PROCESSED_DIR, OUTPUT_XLSX_FILE)
with pd.ExcelWriter(output_xlsx_path, engine="openpyxl") as writer:
    for sheet_name, df in xlsx_sheets.items():
        df.to_excel(writer, sheet_name=sheet_name[:31], index=False)  # 시트 이름 31자 제한
print(f"📁 XLSX 저장 완료: {output_xlsx_path}")
