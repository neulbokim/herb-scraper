import os
import pandas as pd
from modules.string_api import get_string_ids
from modules.data_utils import save_to_json

# ✅ 저장 경로 설정
STRING_DATA_DIR = "data/string"
os.makedirs(STRING_DATA_DIR, exist_ok=True)

# ✅ 입력 및 출력 파일
INPUT_FILE = "data/xlsx/염증 타겟단백질 합집합_250217.csv"
OUTPUT_FILE = os.path.join(STRING_DATA_DIR, "string_id_map_250217.json")

# ✅ CSV 파일 로드
df = pd.read_csv(INPUT_FILE)

# ✅ Gene Name 및 UniProt ID 추출 (둘 다 있는 경우 UniProt ID 우선)
if "UniProt ID" in df.columns and "Gene Name" in df.columns:
    identifiers = df["UniProt ID"].fillna(df["Gene Name"]).dropna().tolist()
elif "UniProt ID" in df.columns:
    identifiers = df["UniProt ID"].dropna().tolist()
elif "Gene Name" in df.columns:
    identifiers = df["Gene Name"].dropna().tolist()
else:
    raise ValueError("CSV 파일에 'Gene Name' 또는 'UniProt ID' 컬럼이 없습니다.")

# ✅ STRING API 호출 (ID 변환)
new_string_ids = get_string_ids(identifiers)

# ✅ JSON으로 저장 (전체 응답 저장)
save_to_json(new_string_ids, "string_api_results_250217.json", subdir="string")

print(f"📁 STRING API 응답을 그대로 저장 완료: {OUTPUT_FILE}")
print(f"✅ 저장된 STRING 데이터 개수: {len(new_string_ids)}")
