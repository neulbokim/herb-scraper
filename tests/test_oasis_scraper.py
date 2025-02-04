import unittest
from unittest.mock import patch
from crawler.oasis_scraper import OasisScraper
from crawler.utils import fetch_html

class TestOasisScraper(unittest.TestCase):
    def setUp(self):
        """테스트 실행 전 OasisScraper 인스턴스 생성"""
        self.scraper = OasisScraper()

    @patch("crawler.utils.fetch_html")
    def test_fetch_page(self, mock_fetch_html):
        """오아시스 약재백과 메인 페이지가 정상적으로 로드되는지 테스트 (Mocking)"""
        mock_html = '<section id="content">Sample HTML Content</section>'
        mock_fetch_html.return_value = mock_html  # 가짜 HTML 반환

        html = fetch_html(self.scraper.base_url)  # 유틸리티 함수 호출
        self.assertIsNotNone(html)
        self.assertIn("<section id=\"content\">", html)

    def test_extract_herb_links(self):
        """샘플 HTML에서 특정 약재(황금, 지황 등)의 상세보기 링크를 제대로 찾는지 테스트"""
        sample_html = """
        <ul class="bul_bar theme_list index1">
            <li>
                <a href="javascript:monoDetailView('370', '1', '지황');" title="지황 상세보기">지황</a>
            </li>
            <li>
                <a href="javascript:monoDetailView('371', '1', '황금');" title="황금 상세보기">황금</a>
            </li>
        </ul>
        """
        herb_links = self.scraper.extract_herb_links(sample_html)

        self.assertIn("지황", herb_links)
        self.assertIn("황금", herb_links)

if __name__ == "__main__":
    unittest.main()
