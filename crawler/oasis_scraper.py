import os
from bs4 import BeautifulSoup
from config import BASE_URL_OASIS, HERBS_TO_SCRAPE
from crawler.utils import fetch_html, save_html, delay_request

class OasisScraper:
    def __init__(self):
        self.base_url = BASE_URL_OASIS
        self.raw_path = "data/raw"
        self.processed_path = "data/processed"
        os.makedirs(self.raw_path, exist_ok=True)
        os.makedirs(self.processed_path, exist_ok=True)

    def extract_herb_links(self, html):
        """HTML에서 약재 상세보기 링크 추출"""
        soup = BeautifulSoup(html, "lxml")
        herb_links = {}
        
        for li in soup.select("ul.bul_bar.theme_list li a"):
            herb_name = li.text.strip()
            if herb_name in HERBS_TO_SCRAPE:
                link = li["href"]
                idx = link.split("'")[1]  # monoDetailView('370', '1', '지황')
                detail_url = f"https://oasis.kiom.re.kr/oasis/herb/monoDetailView_M01.jsp?idx={idx}&tab=1&keyword={herb_name}"
                herb_links[herb_name] = detail_url
        
        return herb_links

    def scrape_oasis(self):
        """오아시스 약재 상세페이지 크롤링"""
        print(f"[INFO] Fetching: {self.base_url}")
        html = fetch_html(self.base_url)
        if not html:
            return None
        
        save_html(html, "oasis_main.html")  # HTML 저장
        herb_links = self.extract_herb_links(html)
        
        for herb, url in herb_links.items():
            print(f"[INFO] Fetching {herb}: {url}")
            herb_html = fetch_html(url)
            if herb_html:
                save_html(herb_html, f"{herb}.html", self.raw_path)
            delay_request(2)  # 2초 대기
        
        return herb_links

if __name__ == "__main__":
    scraper = OasisScraper()
    scraper.scrape_oasis()
