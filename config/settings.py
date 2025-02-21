# config/settings.py

import os

# 📂 기본 경로 설정
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 📁 데이터 디렉토리
DATA_DIR = os.path.join(BASE_DIR, "data")
TCMSP_DIR = os.path.join(DATA_DIR, "tcmsp")

# 📝 파일명 및 그룹 이름
HERB_GROUP_NAME = "전체_약재"

# 🔗 TCMSP BASE URL
#TCMSP_BASE_URL = "https://tcmsp-e.com/tcmspsearch.php"

# ⚙️ 필터링 임계값
OB_THRESHOLD = 30
DL_THRESHOLD = 0.18

# 🗒️ 데이터 경로
RAW_DATA_FILE = f"tcmsp_raw_results_{HERB_GROUP_NAME}.json"
PROCESSED_EXCEL_FILE = f"tcmsp_filtered_targets_{HERB_GROUP_NAME}.xlsx"

# ✅ 데이터 저장 경로
RAW_DATA_PATH = os.path.join(TCMSP_DIR, RAW_DATA_FILE)
PROCESSED_EXCEL_PATH = os.path.join(TCMSP_DIR, PROCESSED_EXCEL_FILE)
