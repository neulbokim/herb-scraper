# modules/constants/herbs.py

# 🌿 약재명과 해당 TCMSP URL 관리
HERB_URLS = {
    "고삼": "https://tcmsp-e.com/tcmspsearch.php?qr=Sophorae%20Flavescentis%20Radix&qsr=herb_en_name",
    "자초": "https://tcmsp-e.com/tcmspsearch.php?qr=Lithospermum%20Erythrorhizon&qsr=herb_en_name",
    "지모": "https://tcmsp-e.com/tcmspsearch.php?qr=Anemarrhenae%20Rhizoma&qsr=herb_en_name"
}

# ✅ 약재명만 리스트로 사용하고 싶을 때
HERB_LIST = list(HERB_URLS.keys())
