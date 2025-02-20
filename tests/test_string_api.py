# tests/test_string_api.py

import pytest
from modules.string_api import fetch_string_ids, fetch_ppi_data, fetch_compound_targets

@pytest.mark.parametrize("gene_names", [["TP53", "EGFR", "TNF"]])
def test_string_id_fetcher(gene_names):
    """✅ STRING ID 조회 테스트"""
    result = fetch_string_ids(gene_names)
    assert result and len(result) == len(gene_names), "❌ STRING ID 조회 실패"

@pytest.mark.parametrize("string_ids", [["9606.ENSP00000269305", "9606.ENSP00000354587"]])
def test_string_ppi_fetcher(string_ids):
    """✅ STRING PPI 데이터 조회 테스트"""
    result = fetch_ppi_data(string_ids)
    assert result and len(result) > 0, "❌ PPI 데이터 조회 실패"

@pytest.mark.parametrize("compounds", [["CCO", "CCC=O"]])
def test_compound_target_fetcher(compounds):
    """✅ 화합물-타겟 단백질 조회 테스트"""
    result = fetch_compound_targets(compounds)
    assert result and len(result) > 0, "❌ 화합물-타겟 조회 실패"
