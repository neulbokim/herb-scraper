import unittest
from unittest.mock import patch
from crawler.pubchem_scraper import PubChemScraper
from crawler.utils import fetch_html

class TestPubChemScraper(unittest.TestCase):
    def setUp(self):
        """테스트 실행 전 PubChemScraper 인스턴스 생성"""
        self.scraper = PubChemScraper()

    @patch("crawler.utils.fetch_html")
    def test_fetch_smiles_valid(self, mock_fetch_html):
        """PubChem에서 유효한 PubChemID로 SMILES 정보를 가져오는지 테스트"""
        mock_html = '<div id="SMILES"><div class="break-words space-y-1">CC(C)CO</div></div>'
        mock_fetch_html.return_value = mock_html

        smiles = self.scraper.fetch_smiles("21629996")  # 가짜 PubChem ID
        self.assertIsNotNone(smiles)
        self.assertEqual(smiles, "CC(C)CO")

    def test_extract_pubchem_id_from_oasis(self):
        """오아시스 상세 페이지에서 PubChem ID를 올바르게 추출하는지 테스트"""
        sample_html = """
        <table class="tstyle_list">
            <tr>
                <td>Baicalein</td>
                <td><a href="https://pubchem.ncbi.nlm.nih.gov/compound/5281605">5281605</a></td>
            </tr>
        </table>
        """
        pubchem_data = self.scraper.extract_pubchem_id_from_oasis(sample_html)
        self.assertIn("Baicalein", pubchem_data)
        self.assertEqual(pubchem_data["Baicalein"], "5281605")

if __name__ == "__main__":
    unittest.main()
