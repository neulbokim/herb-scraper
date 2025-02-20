import os
import json
import pandas as pd
from modules.data_utils import load_from_json

# 입력 및 출력 파일 경로 설정
INPUT_JSON_FILE = "final_merged_results_청열약.json"
OUTPUT_JSON_FILE = "filtered_active_compounds_청열약.json"
OUTPUT_XLSX_FILE = "filtered_active_compounds_청열약.xlsx"
PROCESSED_DIR = "processed"

# 활성 성분 필터링 기준
TPSA_THRESHOLD = 140
BIOAVAILABILITY_THRESHOLD = 0.55
LIPINSKI_MAX_VIOLATION = 1
REQUIRED_DRUGLIKENESS_YES = 4  # 최소 2개 이상 Yes 필요

# JSON 데이터 불러오기
data = load_from_json(INPUT_JSON_FILE, subdir=PROCESSED_DIR)

# 데이터 구조 확인
if isinstance(data, str):  
    data = json.loads(data)  # 문자열이면 JSON으로 변환

filtered_compounds = []

# 데이터가 딕셔너리 구조이면 키(약재명)별로 접근
if isinstance(data, dict):
    for herb_name, ingredients in data.items():
        for compound in ingredients:
            try:
                # TPSA 값 처리 (숫자로 변환 가능하도록 예외 처리)
                tpsa_str = compound.get("TPSA", "0").replace("Å²", "").strip()  # "Å²" 제거 후 공백 제거
                tpsa = float(tpsa_str) if tpsa_str else 0.0  # 빈 값이면 기본값 0.0
                
                gi_absorption = compound.get("GI absorption", "") == "High"
                bioavailability = float(compound.get("Bioavailability Score", "0") or 0.0)
                lipinski = compound.get("Lipinski", "").startswith("Yes") and compound.get("Lipinski", "").count("violation") <= LIPINSKI_MAX_VIOLATION
                
                # Druglikeness 판단
                druglikeness_yes_count = sum([
                    compound.get("Ghose", "") == "Yes",
                    compound.get("Veber", "") == "Yes",
                    compound.get("Egan", "") == "Yes",
                    compound.get("Muegge", "") == "Yes"
                ])
                druglikeness_pass = lipinski and druglikeness_yes_count >= REQUIRED_DRUGLIKENESS_YES
                
                # PAINS alert 확인
                pains_alert = compound.get("PAINS", "") == "0 alert"
                
                # 최종 필터링 적용
                if tpsa < TPSA_THRESHOLD and gi_absorption and druglikeness_pass and bioavailability >= BIOAVAILABILITY_THRESHOLD and pains_alert:
                    compound["Herb"] = herb_name  # 약재명 추가
                    filtered_compounds.append(compound)
            except Exception as e:
                print(f"⚠️ Error processing compound {compound.get('Ingredient Name', 'Unknown')}: {e}")

else:
    print("⚠️ Unexpected JSON structure: Expected dictionary with herbs as keys.")

# 타겟 단백질 정보를 개별 행으로 변환하는 과정
expanded_rows = []
for compound in filtered_compounds:
    targets = compound.get("Targets", [])
    if targets:
        for target in targets:
            new_compound = compound.copy()
            new_compound["Gene ID"] = target.get("gene_id", "")
            new_compound["Gene Name"] = target.get("gene_name", "")
            new_compound["Score"] = target.get("score", "")
            expanded_rows.append(new_compound)
    else:
        compound["Gene ID"] = ""
        compound["Gene Name"] = ""
        compound["Score"] = ""
        expanded_rows.append(compound)

# 데이터프레임 생성
df = pd.DataFrame(expanded_rows)

# 필요 없는 "Targets" 컬럼 삭제
df.drop(columns=["Targets"], inplace=True, errors='ignore')

# JSON 저장
output_json_path = os.path.join("data", PROCESSED_DIR, OUTPUT_JSON_FILE)
with open(output_json_path, "w", encoding="utf-8") as f:
    json.dump(expanded_rows, f, ensure_ascii=False, indent=4)

# XLSX 저장
output_xlsx_path = os.path.join("data", PROCESSED_DIR, OUTPUT_XLSX_FILE)
df.to_excel(output_xlsx_path, index=False, engine="openpyxl")

print(f"✅ 변환 완료: {output_json_path}, {output_xlsx_path}")
