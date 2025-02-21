# tests/test_preprocessors.py

import pytest
from modules.preprocessors import filter_active_compounds, merge_herb_data, map_targets_to_ingredients
from modules.utils import save_to_json, load_from_json
from pathlib import Path

@pytest.fixture
def sample_ingredients():
    return [
        {"ingredient": "baicalin", "TPSA": 50, "GI absorption": "High"},
        {"ingredient": "berberine", "TPSA": 150, "GI absorption": "Low"},
        {"ingredient": "geniposide", "TPSA": 100, "GI absorption": "High"},
    ]

def test_filter_active_compounds(tmp_path, sample_ingredients):
    """✅ 활성 성분 필터링 테스트 (TPSA < 120)"""
    output_file = tmp_path / "filtered.json"
    filter_active_compounds(sample_ingredients, tpsa_threshold=120, output_file=str(output_file))
    filtered = load_from_json(str(output_file))

    assert len(filtered) == 2, "❌ 필터링 실패"
    assert all(c["TPSA"] < 120 for c in filtered), "❌ TPSA 기준 적용 실패"

def test_merge_herb_data(tmp_path, sample_ingredients):
    """✅ HERB 데이터 병합 테스트"""
    herb_file = tmp_path / "herb.json"
    swissadme_file = tmp_path / "swissadme.json"
    save_to_json(sample_ingredients, str(herb_file))
    save_to_json(sample_ingredients, str(swissadme_file))

    output_file = tmp_path / "merged.json"
    merge_herb_data(str(herb_file), str(swissadme_file), output_file=str(output_file))
    merged = load_from_json(str(output_file))

    assert len(merged) == len(sample_ingredients), "❌ 데이터 병합 실패"
