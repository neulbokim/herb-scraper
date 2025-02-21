# tests/test_converters.py

import pytest
from modules.converters import convert_to_csv, convert_to_xlsx, convert_to_json
from modules.utils import save_to_json, load_csv
from pathlib import Path

@pytest.fixture
def sample_ingredients():
    return [
        {"ingredient": "baicalin", "SMILES": "CCO"},
        {"ingredient": "wogonin", "SMILES": "CCC=O"},
    ]

def test_convert_to_csv(tmp_path, sample_ingredients):
    """✅ JSON → CSV 변환 테스트"""
    input_file = tmp_path / "sample.json"
    output_file = tmp_path / "sample.csv"
    save_to_json(sample_ingredients, str(input_file))

    convert_to_csv(str(input_file), str(output_file))
    assert output_file.exists(), "❌ CSV 파일 생성 실패"

def test_convert_to_xlsx(tmp_path, sample_ingredients):
    """✅ JSON → XLSX 변환 테스트"""
    input_file = tmp_path / "sample.json"
    output_file = tmp_path / "sample.xlsx"
    save_to_json(sample_ingredients, str(input_file))

    convert_to_xlsx(str(input_file), str(output_file))
    assert output_file.exists(), "❌ XLSX 파일 생성 실패"

def test_convert_to_json(tmp_path):
    """✅ CSV → JSON 변환 테스트"""
    csv_content = "ingredient,SMILES\nbaicalin,CCO\nwogonin,CCC=O"
    csv_file = tmp_path / "sample.csv"
    csv_file.write_text(csv_content, encoding="utf-8")

    output_file = tmp_path / "converted.json"
    convert_to_json(str(csv_file), str(output_file))
    assert output_file.exists(), "❌ JSON 변환 실패"
