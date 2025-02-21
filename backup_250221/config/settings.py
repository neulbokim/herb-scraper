# config/settings.py

import os

# 📁 프로젝트 경로 설정
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 📂 데이터 경로 설정
DATA_DIR = os.path.join(BASE_DIR, "data")
RAW_DIR = os.path.join(DATA_DIR, "raw")
PROCESSED_DIR = os.path.join(DATA_DIR, "processed")

# 📥 RAW 데이터 경로 (TCMSP 전용)
TCMSP_RAW_DIR = os.path.join(RAW_DIR, "tcmsp", "raw_results")

# 📝 PROCESSED 데이터 경로 (향후 필요 시 사용)
FINAL_DIR = os.path.join(PROCESSED_DIR, "final")
FINAL_CSV_DIR = os.path.join(FINAL_DIR, "csv")
FINAL_XLSX_DIR = os.path.join(FINAL_DIR, "xlsx")
FINAL_JSON_DIR = os.path.join(FINAL_DIR, "json")

# 🕒 크롤링 및 API 옵션
SELENIUM_TIMEOUT = 10
API_TIMEOUT = 15
REQUEST_DELAY = 1

# 🗒️ 파일명 규칙
DEFAULT_TCMSP_RESULT_FILE = "tcmsp_results_{herb_name}.json"
DEFAULT_TCMSP_TARGET_FILE = "tcmsp_targets_{herb_name}.json"

FILENAME_RULES = {
    "tcmsp_results": DEFAULT_TCMSP_RESULT_FILE,
    "tcmsp_targets": DEFAULT_TCMSP_TARGET_FILE,
}
