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
    save_to_json(data, filename, subdir)  # JSON 저장 기본

    # CSV 및 Excel 저장 (옵션에 따라 추가 가능)
    save_to_csv(data, filename.replace(".json", ".csv"), subdir)
    save_to_excel(data, filename.replace(".json", ".xlsx"), subdir)
