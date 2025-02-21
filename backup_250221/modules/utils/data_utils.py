#modules/utils/data_utils.py

import pandas as pd
import os

def save_to_csv(data, filename, subdir):
    """
    📝 CSV 파일로 데이터를 저장
    """
    file_path = os.path.join(subdir, filename)
    df = pd.DataFrame(data)
    df.to_csv(file_path, index=False)
    print(f"✅ {filename}: CSV 저장 완료")

def save_to_excel(data, filename, subdir):
    """
    📝 Excel 파일로 데이터를 저장
    """
    file_path = os.path.join(subdir, filename)
    df = pd.DataFrame(data)
    df.to_excel(file_path, index=False)
    print(f"✅ {filename}: Excel 저장 완료")
    
def save_data(data, filename, subdir):
    """
    📝 데이터를 파일로 저장 (JSON, CSV, Excel 지원)
    """
    # JSON 저장
    save_to_json(data, filename, subdir)

    # CSV 및 Excel 저장 (옵션에 따라 추가 가능)
    save_to_csv(data, filename.replace(".json", ".csv"), subdir)
    save_to_excel(data, filename.replace(".json", ".xlsx"), subdir)

def load_from_json(file_path: str):
    """📥 JSON 파일 로드"""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        logger.info(f"✅ JSON 로드 완료 → {file_path}")
        return data
    except Exception as e:
        logger.error(f"❌ JSON 로드 실패: {file_path} | {e}")
        return None

def save_to_json(data: list, file_path: str):
    """💾 JSON 파일 저장"""
    try:
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        logger.info(f"✅ JSON 저장 완료 → {file_path}")
    except Exception as e:
        logger.error(f"❌ JSON 저장 실패: {file_path} | {e}")
        
def load_csv(file_path: str):
    """📥 CSV 파일 로드"""
    try:
        df = pd.read_csv(file_path)
        logger.info(f"✅ CSV 로드 완료 → {file_path}")
        return df
    except Exception as e:
        logger.error(f"❌ CSV 로드 실패: {file_path} | {e}")
        return pd.DataFrame()