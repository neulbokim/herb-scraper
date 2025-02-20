# tests/test_utils.py

import pytest
from modules.utils import save_to_json, load_from_json, save_to_csv, load_csv
import os

@pytest.fixture
def sample_data():
    return [{"herb": "황금", "ingredient": "baicalin"}, {"herb": "황련", "ingredient": "berberine"}]

def test_save_and_load_json(tmp_path, sample_data):
    """✅ JSON 저장 및 로드 테스트"""
    file_path = tmp_path / "sample.json"
    save_to_json(sample_data, str(file_path))
    loaded_data = load_from_json(str(file_path))

    assert loaded_data == sample_data, "❌ JSON 저장/로드 실패"

def test_save_and_load_csv(tmp_path, sample_data):
    """✅ CSV 저장 및 로드 테스트"""
    file_path = tmp_path / "sample.csv"
    save_to_csv(sample_data, str(file_path))
    loaded_df = load_csv(str(file_path))

    assert not loaded_df.empty, "❌ CSV 로드 실패"
    assert list(loaded_df.columns) == ["herb", "ingredient"], "❌ CSV 컬럼 불일치"
