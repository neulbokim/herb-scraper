# modules/constants/apis.py

# 🔗 API URL 설정
BATMAN_TCM_API_URL = "http://batman2api.cloudna.cn/queryTarget"
SWISSADME_URL = "http://www.swissadme.ch/"
SWISSTARGET_URL = "http://www.swisstargetprediction.ch/"
TCMSP_BASE_URL = "https://tcmsp-e.com/tcmspsearch.php"

# 🧬 STRING API URL
STRING_ID_API_URL = "https://string-db.org/api/json/get_string_ids"
STRING_PPI_API_URL = "https://string-db.org/api/json/network"
COMPOUND_TARGET_API_URL = "https://string-db.org/api/json/compound_target"

# ⏳ API 요청 타임아웃 설정
API_TIMEOUTS = {
    "BATMAN_TCM": 10,
    "SWISSADME": 10,
    "SWISSTARGET": 10,
    "TCMSP": 15,
    "STRING": 10,
}

# 📝 HTTP 요청 헤더 설정
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    )
}
