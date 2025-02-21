# 📁 프로젝트 경로 설정
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 📂 데이터 경로 설정
DATA_DIR = os.path.join(BASE_DIR, "data")
RAW_DIR = os.path.join(DATA_DIR, "raw")
PROCESSED_DIR = os.path.join(DATA_DIR, "processed")
FINAL_DIR = os.path.join(PROCESSED_DIR, "final")

# 📥 RAW 데이터 세부 경로
TCMSP_RAW_DIR = os.path.join(RAW_DIR, "tcmsp", "raw_results")

# 📝 PROCESSED 데이터 경로
FILTERED_DIR = os.path.join(PROCESSED_DIR, "filtered")
MERGED_DIR = os.path.join(PROCESSED_DIR, "merged")

# 📊 최종 데이터 저장 경로
FINAL_CSV_DIR = os.path.join(FINAL_DIR, "csv")
FINAL_XLSX_DIR = os.path.join(FINAL_DIR, "xlsx")
FINAL_JSON_DIR = os.path.join(FINAL_DIR, "json")

# 🌍 크롤링 및 API 옵션
SELENIUM_TIMEOUT = 10
API_TIMEOUT = 10
REQUEST_DELAY = 1

# 🗒️ 파일명 규칙 (일관성 확보)
DEFAULT_TCMSP_RESULT_FILE = "tcmsp_results_{herb_name}.json"
DEFAULT_TCMSP_TARGET_FILE = "tcmsp_targets_{herb_name}.json"

# ✅ 파일명 설정 (사용자가 원하는 이름으로 재정의 가능)
FILENAME_RULES = {
    "tcmsp_results": DEFAULT_TCMSP_RESULT_FILE,
    "tcmsp_targets": DEFAULT_TCMSP_TARGET_FILE
}
