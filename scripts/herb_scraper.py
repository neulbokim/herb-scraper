from modules.data_utils import save_to_json
from modules.herb_utils import get_all_ingredient_links
import os

HERB_URLS = {
    "지황": "http://herb.ac.cn/Detail/?v=HERB001251&label=Herb",
  }

def main():
    """한약재 성분 URL 크롤링 (1단계)"""
    all_ingredient_urls = {}

    for herb_name, herb_url in HERB_URLS.items():
        print(f"🌿 {herb_name} 크롤링 시작: {herb_url}")
        ingredient_links = get_all_ingredient_links(herb_url)

        if ingredient_links:
            all_ingredient_urls[herb_name] = ingredient_links
            print(f"✅ {herb_name} 성분 URL {len(ingredient_links)}개 수집 완료!")

    # ✅ subdir="raw" 제거 (data/raw에 자동 저장)
    save_to_json(all_ingredient_urls, f"herb_ingredient_urls_지황.json", subdir="herb")

if __name__ == "__main__":
    main()