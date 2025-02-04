from bs4 import BeautifulSoup
from crawler.utils import post_html

class SwissAdmeScraper:
    def fetch_molecule_data(self, smiles):
        """SwissADME에서 모든 분자 특성 정보 가져오기"""
        # SMILES 검색 요청
        html = post_html("http://www.swissadme.ch/index.php", {"smiles": smiles})

        if not html:
            print("[ERROR] SwissADME 검색 실패")
            return None

        soup = BeautifulSoup(html, "lxml")
        molecule_info = {}

        # 모든 테이블을 찾음
        tables = soup.find_all("table")

        for table in tables:
            rows = table.find_all("tr")
            for row in rows:
                cols = row.find_all("td")

                if len(cols) == 2:  # 데이터가 있는 행
                    key = cols[0].text.strip()
                    value = cols[1].text.strip()
                    molecule_info[key] = value

        return molecule_info
