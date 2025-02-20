# tests/test_preprocessors.py

import pytest
from modules.preprocessors.filter_compounds import filter_active_compounds
from modules.preprocessors.merge_herb_data import merge_herb_data

@pytest.fixture
def dummy_compounds():
    return [
        {"ingredient": "baicalin", "TPSA": 50, "GI absorption": "High"},
        {"ingredient": "berberine", "TPSA": 150, "GI absorption": "Low"},
        {"ingredient": "geniposide", "TPSA": 100, "GI absorption": "High"}
    ]

@pytest.fixture
def dummy_herb_data():
    return [
        {"herb": "황금", "ingredient": "baicalin"},
        {"herb": "황련", "ingredient": "berberine"},
        {"herb": "치자", "ingredient": "geniposide"}
    ]

def test_filter_active_compounds(dummy_compounds):
    """✅ 활성 성분 필터링 테스트 (TPSA < 120)"""
    filtered = filter_active_compounds(dummy_compounds, tpsa_threshold=120)
    assert len(filtered) == 2, "❌ 필터링 실패"

def test_merge_herb_data(dummy_herb_data, dummy_compounds):
    """✅ HERB 데이터 병합 테스트"""
    merged = merge_herb_data([dummy_herb_data, dummy_compounds])
    assert len(merged) == 3, "❌ 데이터 병합 실패"
