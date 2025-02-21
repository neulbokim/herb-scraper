# tests/test_string_api.py

import pytest
from modules.string_api import fetch_string_ids, fetch_ppi_data, fetch_compound_targets

@pytest.fixture
def sample_gene_names():
    return ["TP53", "EGFR"]

@pytest.fixture
def sample_compounds():
    return ["CCO", "CCC=O"]

def test_fetch_string_ids(sample_gene_names):
    """✅ STRING ID 조회 테스트"""
    result = fetch_string_ids(sample_gene_names)
    assert result and len(result) == len(sample_gene_names), "❌ STRING ID 조회 실패"

def test_fetch_ppi_data():
    """✅ PPI 데이터 조회 테스트"""
    string_ids = ["9606.ENSP00000269305", "9606.ENSP00000354587"]
    result = fetch_ppi_data(string_ids)
    assert result, "❌ PPI 데이터 조회 실패"

def test_fetch_compound_targets(sample_compounds):
    """✅ 화합물-타겟 단백질 매핑 테스트"""
    result = fetch_compound_targets(sample_compounds)
    assert result, "❌ 화합물-타겟 조회 실패"
