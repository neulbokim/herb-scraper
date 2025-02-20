# tests/test_converters.py

import pytest
from modules.converters import to_csv, to_xlsx, to_json
from modules.utils import load_from_json, load_csv
import os

@pytest.fixture
def sample_data():
    return [
        {"herb": "황금", "ingredient": "baicalin"},
        {"herb": "황련", "ingredient": "berberine"}
    ]

def test_convert_to_csv(tmp_path, sample_data):
    """✅ JSON → CSV 변환 테스트"""
    json_path = tmp_path / "test_data.json"
    csv_path = tmp_path / "test_data.csv"

    to_json.convert(sample_data, str(json_path))
    to_csv.convert_json_to_csv(str(json_path), str(csv_path))

    assert os.path.exists(csv_path), "❌ CSV 파일 생성 실패"


def test_convert_to_xlsx(tmp_path, sample_data):
    """✅ JSON → XLSX 변환 테스트"""
    json_path = tmp_path / "test_data.json"
    xlsx_path = tmp_path / "test_data.xlsx"

    to_json.convert(sample_data, str(json_path))
    to_xlsx.convert_json_to_xlsx(str(json_path), str(xlsx_path))

    assert os.path.exists(xlsx_path), "❌ XLSX 파일 생성 실패"


def test_convert_to_json(tmp_path):
    """✅ CSV → JSON 변환 테스트"""
    csv_path = tmp_path / "test_data.csv"
    json_path = tmp_path / "converted_data.json"

    sample_csv_content = "herb,ingredient\n황금,baicalin\n황련,berberine"
    csv_path.write_text(sample_csv_content, encoding="utf-8")

    to_json.convert_csv_to_json(str(csv_path), str(json_path))

    assert os.path.exists(json_path), "❌ JSON 파일 생성 실패"
