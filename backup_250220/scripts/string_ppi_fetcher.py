import os
import json
import csv
from modules.data_utils import save_to_json, load_from_json
from modules.string_api import get_ppi_data  # ✅ STRING API 모듈 사용

# ✅ 저장 경로 설정
STRING_DATA_DIR = "data/string"
os.makedirs(STRING_DATA_DIR, exist_ok=True)

# ✅ 입력 및 출력 파일
STRING_API_RESULTS_FILE = os.path.join(STRING_DATA_DIR, "string_api_results_250217.json")
PPI_JSON_FILE = os.path.join(STRING_DATA_DIR, "string_ppi_results_250217.json")
PPI_CSV_FILE = os.path.join(STRING_DATA_DIR, "string_ppi_results_250217.csv")


def load_string_ids():
    """STRING API 결과 파일에서 STRING ID 리스트 추출"""
    if not os.path.exists(STRING_API_RESULTS_FILE):
        raise FileNotFoundError(f"⚠️ 파일 없음: {STRING_API_RESULTS_FILE}")

    with open(STRING_API_RESULTS_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

    # ✅ STRING ID만 추출하여 리스트 생성
    string_ids = [entry["stringId"] for entry in data if "stringId" in entry]
    return string_ids


# ✅ STRING ID 가져오기
string_ids = load_string_ids()

if not string_ids:
    print("⚠️ 가져올 STRING ID가 없습니다.")
else:
    print(f"🔹 가져온 STRING ID 개수: {len(string_ids)}")
    print(f"🔹 첫 10개 STRING ID: {string_ids[:10]}")  # ✅ STRING ID 확인

    # ✅ PPI 데이터 가져오기 (modules/string_api.py의 get_ppi_data 함수 사용)
    ppi_data = get_ppi_data(string_ids)

    if ppi_data:
        # ✅ JSON 저장
        save_to_json(ppi_data, "string_ppi_results_250217.json", subdir="string")

        # ✅ CSV 저장
        with open(PPI_CSV_FILE, "w", newline="") as csvfile:
            csv_writer = csv.writer(csvfile)
            csv_writer.writerow(["STRING ID A", "STRING ID B", "Protein A", "Protein B", "NCBI Taxon ID", "Combined Score"])
            for row in ppi_data:
                csv_writer.writerow(row.values())

        print(f"✅ PPI 데이터가 {PPI_CSV_FILE} 및 {PPI_JSON_FILE}에 저장되었습니다.")
    else:
        print("⚠️ 유효한 PPI 데이터가 없습니다. 저장하지 않습니다.")
