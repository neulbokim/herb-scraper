# tests/test_crawlers.py

import pytest
from modules.crawlers.herb_crawler import crawl_herb_data
from modules.crawlers.swissadme_crawler import crawl_swissadme
from modules.constants.herbs import HERB_LIST
from modules.utils import load_from_json
from config.settings import HERB_RAW_DIR, SWISSADME_RAW_DIR
import os

@pytest.mark.parametrize("herb_name", HERB_LIST[:3])  # 첫 3개 약재만 테스트
def test_herb_crawler(herb_name):
    """✅ HERB 크롤링 테스트"""
    crawl_herb_data(herb_name)
    file_path = os.path.join(HERB_RAW_DIR, f"herb_ingredient_urls_{herb_name}.json")
    assert os.path.exists(file_path), f"❌ {file_path} 생성 실패"


def test_swissadme_crawler():
    """✅ SwissADME 크롤링 테스트 (더미 데이터 사용)"""
    dummy_ingredients = ["CCO", "CCC=O", "CCCN"]
    crawl_swissadme("테스트용_약재", dummy_ingredients)
    file_path = os.path.join(SWISSADME_RAW_DIR, "swissadme_results_테스트용_약재.json")
    assert os.path.exists(file_path), "❌ SwissADME 결과 파일 생성 실패"
