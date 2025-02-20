from modules.data_utils import save_to_json
from modules.herb_utils import get_all_ingredient_links
import os

HERB_URLS = {
    "황금": "http://herb.ac.cn/Detail/?v=HERB002563&label=Herb",
    "황련": "http://herb.ac.cn/Detail/?v=HERB002540&label=Herb",
    "지황": "http://herb.ac.cn/Detail/?v=HERB001251&label=Herb",
    "치자": "http://herb.ac.cn/Detail/?v=HERB007046&label=Herb",
    "황백": "http://herb.ac.cn/Detail/?v=HERB002489&label=Herb",
    "자초": "http://herb.ac.cn/Detail/?v=HERB007160&label=Herb",
    "고삼": "http://herb.ac.cn/Detail/?v=HERB003164&label=Herb",
    "지모": "http://herb.ac.cn/Detail/?v=HERB007023&label=Herb",
    #"인삼": "http://herb.ac.cn/Detail/?v=HERB004609&label=Herb",
    #"파두": "http://herb.ac.cn/Detail/?v=HERB000129&label=Herb",
    #"마황": "http://herb.ac.cn/Detail/?v=HERB003658&label=Herb",
    #"과체": "http://herb.ac.cn/Detail/?v=HERB001948&label=Herb",
    #"오미자": "http://herb.ac.cn/Detail/?v=HERB005762&label=Herb",
    #"차전": "http://herb.ac.cn/Detail/?v=HERB000766&label=Herb"
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
    save_to_json(all_ingredient_urls, f"herb_ingredient_urls_8약재.json")

if __name__ == "__main__":
    main()