import os
import pandas as pd
from modules.data_utils import load_from_json

def convert_json_to_single_xlsx(herb_names, output_filename="swissadme_results.xlsx"):
    """여러 약재 JSON 데이터를 하나의 XLSX 파일에 각 시트로 저장"""

    input_dir = "data/processed"
    output_dir = "data/xlsx"
    os.makedirs(output_dir, exist_ok=True)  # xlsx 저장 폴더 생성

    output_path = os.path.join(output_dir, output_filename)

    with pd.ExcelWriter(output_path, engine="openpyxl") as writer:
        for herb_name in herb_names:
            try:
                input_filename = f"swissadme_processed_results_{herb_name}.json"

                # JSON 파일 불러오기
                data = load_from_json(input_filename, subdir="processed")
                if not data:
                    print(f"⚠️ {herb_name}: 파일 {input_filename} 이(가) 비어 있거나 존재하지 않습니다.")
                    continue

                # JSON → DataFrame 변환
                df = pd.json_normalize(data, sep="_")  # 중첩된 데이터 필드명 정리

                # 엑셀 파일에 새로운 시트로 저장
                df.to_excel(writer, sheet_name=herb_name[:31], index=False)  # 시트 이름 31자 제한
                print(f"✅ {herb_name}: 시트 저장 완료")

            except Exception as e:
                print(f"❌ {herb_name}: 변환 중 오류 발생: {e}")

    print(f"📁 최종 엑셀 저장 완료: {output_path}")

if __name__ == "__main__":
    herb_names = ["인삼", "파두", "마황", "오미자", "차전"]  # 변환할 약재 리스트
    convert_json_to_single_xlsx(herb_names)
