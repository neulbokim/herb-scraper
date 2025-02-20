import os
import pandas as pd
from modules.data_utils import load_from_json, save_to_json

def json_to_csv(input_json, output_csv, subdir="processed"):
    data = load_from_json(input_json, subdir)
    if not data:
        print(f"⚠️ {input_json} 데이터 없음.")
        return
    pd.DataFrame(data).to_csv(os.path.join("data", subdir, output_csv), index=False)
    print(f"✅ 저장 완료: {output_csv}")

def json_to_xlsx(input_json, output_xlsx, subdir="processed"):
    data = load_from_json(input_json, subdir)
    if not data:
        print(f"⚠️ {input_json} 데이터 없음.")
        return
    pd.DataFrame(data).to_excel(os.path.join("data", subdir, output_xlsx), index=False)
    print(f"✅ 저장 완료: {output_xlsx}")

def csv_to_xlsx(input_csv, output_xlsx, subdir="processed"):
    df = pd.read_csv(os.path.join("data", subdir, input_csv))
    df.to_excel(os.path.join("data", subdir, output_xlsx), index=False)
    print(f"✅ 저장 완료: {output_xlsx}")
