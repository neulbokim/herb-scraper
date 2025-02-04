import unittest
from unittest.mock import patch
from crawler.swissadme_scraper import SwissAdmeScraper
from crawler.utils import post_html

class TestSwissAdmeScraper(unittest.TestCase):
    def setUp(self):
        """테스트 실행 전 SwissAdmeScraper 인스턴스 생성"""
        self.scraper = SwissAdmeScraper()

    @patch("crawler.utils.post_html")
    def test_fetch_molecule_data_valid(self, mock_post_html):
        """유효한 SMILES 문자열을 SwissADME에 입력했을 때 분자 정보를 정상적으로 가져오는지 테스트"""
        mock_html = """
        <table>
            <tr><td>Formula</td><td>C31H38O16</td></tr>
            <tr><td>Molecular weight</td><td>666.62 g/mol</td></tr>
        </table>
        """
        mock_post_html.return_value = mock_html

        smiles = "CC(=O)Oc1ccccc1C(=O)O"
        molecule_info = self.scraper.fetch_molecule_data(smiles)

        self.assertIsNotNone(molecule_info)
        self.assertIn("Formula", molecule_info)
        self.assertEqual(molecule_info["Formula"], "C31H38O16")

if __name__ == "__main__":
    unittest.main()
