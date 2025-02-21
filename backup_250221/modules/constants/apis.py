# modules/constants/apis.py

# 🔗 TCMSP URL 설정
TCMSP_BASE_URL = "https://tcmsp-e.com/tcmspsearch.php"

# ⏳ API 요청 타임아웃 설정
API_TIMEOUTS = {
    "TCMSP": 8,  # seconds
}

# 📝 HTTP 요청 헤더 설정
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    )
}
