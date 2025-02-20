import os
import json
import pandas as pd
from modules.data_utils import load_from_json

# 입력 및 출력 파일 경로 설정
INPUT_JSON_FILE = "batman_tcm_results.json"
OUTPUT_CSV_FILE = "batman_tcm_results.csv"
RAW_DIR = "raw"

# JSON 데이터 불러오기
data = load_from_json(INPUT_JSON_FILE, subdir=RAW_DIR)

# 변환된 데이터를 저장할 리스트
rows = []

# JSON 데이터를 판다스 데이터프레임 형식으로 변환
for item in data:
    base_info = {
        "Herb": item.get("herb_name", ""),
        "Ingredient Name": item.get("ingredient_name", ""),
        "PubChem ID": item.get("PubChem id", ""),
    }

    # batman_tcm_results 필드 처리
    batman_results = item.get("batman_tcm_results", {})

    # batman_tcm_results가 리스트인 경우 첫 번째 요소 사용
    if isinstance(batman_results, list):
        batman_results = batman_results[0] if batman_results else {}

    targets = batman_results.get("target", [])

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

# CSV 저장
output_csv_path = os.path.join("data", RAW_DIR, OUTPUT_CSV_FILE)
df.to_csv(output_csv_path, index=False, encoding="utf-8-sig")

print(f"✅ 변환 완료: {output_csv_path}")
