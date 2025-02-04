from bs4 import BeautifulSoup
from config import BASE_URL_PUBCHEM
from crawler.utils import fetch_html
from crawler.utils import load_html

class PubChemScraper:
    def fetch_smiles(self, pubchem_id):
        """PubChem에서 SMILES 가져오기"""
        url = f"{BASE_URL_PUBCHEM}{pubchem_id}"
        html = fetch_html(url)  # 유틸리티 함수 사용

        if not html:
            return None

        soup = BeautifulSoup(html, "lxml")
        smiles_tag = soup.select_one("#SMILES > div.px-1.py-3.space-y-2 > div.break-words.space-y-1")
        return smiles_tag.text.strip() if smiles_tag else None
        
    def extract_pubchem_id_from_oasis(self, herb_name):
        """오아시스 상세 페이지에서 Name-PubChem ID 목록을 추출"""
        file_path = f"data/raw/{herb_name}.html"
        html = load_html(file_path)

        if not html:
            print(f"[ERROR] {herb_name} 상세 페이지 로드 실패")
            return None

        soup = BeautifulSoup(html, "lxml")
        pubchem_data = {}

        # 테이블 찾기
        table = soup.select_one(".tstyle_list")
        if not table:
            print(f"[WARNING] {herb_name}의 PubChem 테이블을 찾을 수 없음.")
            return None

        # 테이블 데이터 추출
        rows = table.select("tbody tr")
        for row in rows:
            cols = row.find_all("td")
            if len(cols) >= 6:  # 두 쌍의 Name, PubChemID, Reference가 존재
                # 첫 번째 성분
                name1 = cols[0].text.strip()
                pubchem_id1 = cols[1].find("a")
                pubchem_id1 = pubchem_id1.text.strip() if pubchem_id1 else "정보 없음"

                # 두 번째 성분
                name2 = cols[3].text.strip()
                pubchem_id2 = cols[4].find("a")
                pubchem_id2 = pubchem_id2.text.strip() if pubchem_id2 else "정보 없음"

                # 유효한 PubChem ID만 저장
                if pubchem_id1 != "정보 없음":
                    pubchem_data[name1] = pubchem_id1
                if pubchem_id2 != "정보 없음":
                    pubchem_data[name2] = pubchem_id2

        return pubchem_data
