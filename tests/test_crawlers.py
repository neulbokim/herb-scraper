# tests/test_crawlers.py

import pytest
from pathlib import Path
from modules.crawlers import (
    crawl_herb_data,
    crawl_swissadme,
)
from modules.constants.herbs import HERB_LIST
from modules.utils import load_from_json
from config.settings import HERB_RAW_DIR, SWISSADME_RAW_DIR

@pytest.mark.parametrize("herb_name", HERB_LIST[:2])  # 대표 2개만 테스트
def test_crawl_herb_data(herb_name):
    """✅ HERB 크롤링 테스트"""
    crawl_herb_data([herb_name])
    file_path = Path(HERB_RAW_DIR) / f"herb_ingredient_urls_{herb_name}.json"

    assert file_path.exists(), f"❌ {file_path} 생성 실패"

    data = load_from_json(file_path)
    assert len(data) > 0, f"❌ {herb_name} 크롤링 데이터 없음"
    assert all("ingredient_id" in item for item in data), "❌ ingredient_id 없음"
    assert all("molecule_smile" in item for item in data), "❌ molecule_smile 없음"
    assert all(isinstance(item["related_gene_targets"], list) for item in data), "❌ 관련 유전자 리스트 오류"

def test_crawl_swissadme():
    """✅ SwissADME 크롤링 테스트 (샘플 성분 사용)"""
    herb_name = "황금"
    sample_ingredients = [{"ingredient": "baicalin", "SMILES": "CCO"}]
    crawl_swissadme(herb_name, sample_ingredients)
    file_path = Path(SWISSADME_RAW_DIR) / f"swissadme_results_{herb_name}.json"
    assert file_path.exists(), f"❌ SwissADME 결과 파일 생성 실패"
