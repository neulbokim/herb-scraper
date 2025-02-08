import json
from modules.data_utils import load_from_json, save_to_json

def filter_swissadme_data(herb_names):
    """SwissADME 원본 데이터에서 필요한 속성만 필터링하여 저장"""

    if isinstance(herb_names, str):  # 단일 약재명이 들어올 경우 리스트로 변환
        herb_names = [herb_names]

    for herb_name in herb_names:
        try:
            # 파일명 설정
            input_filename = f"swissadme_results_{herb_name}.json"
            output_filename = f"swissadme_processed_results_{herb_name}.json"

            # 데이터 로드 (기본 subdir="raw" 설정)
            data = load_from_json(input_filename, subdir="raw")
            if not data:
                print(f"⚠️ {herb_name}: 파일 {input_filename} 이(가) 비어 있거나 존재하지 않습니다.")
                continue  # 다음 약재 처리

            filtered_data = []

            for item in data:
                try:
                    # 기본 정보 필터링
                    filtered_item = {
                        "ingredient_url": item.get("ingredient_url", ""),
                        "ingredient_name": item.get("ingredient_name", ""),
                        "molecule_smile": item.get("molecule_smile", ""),
                    }

                    # swissadme_results 내부 정보 필터링
                    if "swissadme_results" in item:
                        filtered_item["swissadme_results"] = {
                            "SMILES": item["swissadme_results"].get("SMILES", ""),
                            "Formula": item["swissadme_results"].get("Formula", ""),
                            "TPSA": item["swissadme_results"].get("TPSA", ""),
                            "Lipinski": item["swissadme_results"].get("Lipinski", ""),
                            "Ghose": item["swissadme_results"].get("Ghose", ""),
                            "Veber": item["swissadme_results"].get("Veber", ""),
                            "Egan": item["swissadme_results"].get("Egan", ""),
                            "Muegge": item["swissadme_results"].get("Muegge", ""),
                            "Bioavailability Score": item["swissadme_results"].get("Bioavailability Score", ""),
                        }

                    filtered_data.append(filtered_item)

                except Exception as e:
                    print(f"❌ {herb_name}: 데이터 필터링 중 오류 발생: {e}")

            # 필터링된 데이터 저장 (기본 subdir="processed")
            save_to_json(filtered_data, output_filename, subdir="processed")
            print(f"✅ {herb_name}: 처리된 데이터가 {output_filename}에 저장되었습니다.")

        except Exception as e:
            print(f"❌ {herb_name}: 전체 처리 중 오류 발생: {e}")

if __name__ == "__main__":
    herb_names = ["고삼", "지모", "지황", "치자", "황금", "황련", "황백"]  # 원하는 약재 리스트 입력
    filter_swissadme_data(herb_names)
