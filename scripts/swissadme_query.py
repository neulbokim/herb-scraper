import json
import os
import time
from tqdm import tqdm
from modules.data_utils import load_from_json, save_to_json
from modules.swissadme_utils import get_swissadme_data  # ✅ SwissADME 크롤링 함수 가져오기

def save_swissadme_results(herb_name):
    """SwissADME 데이터를 크롤링하고 저장"""
    input_file = f"herb_ingredients_{herb_name}.json"
    output_file = f"swissadme_results_{herb_name}.json"  # ✅ save_to_json이 subdir="raw" 사용하므로 파일명만 지정

    # ✅ 입력 데이터 로드
    herb_data = load_from_json(input_file)

    # ✅ 유효한 Molecule SMILE 리스트 추출 + 기존 PubChem ID 등 데이터 유지
    ingredient_data = [
        {
            "ingredient_url": url,
            "ingredient_name": data.get("ingredient_name", "N/A"),
            "molecule_smile": data.get("molecule_smile", "not found"),
            **{key: value for key, value in data.items() if key not in ["ingredient_name", "molecule_smile"]}
        }
        for url, data in herb_data.items()
        if isinstance(data, dict) and data.get("molecule_smile") not in ["Not Available", "not found", ""]
    ]

    if ingredient_data:
        print(f"🚀 {herb_name} SwissADME 크롤링 시작!")

        # ✅ SwissADME 크롤링 실행
        results = get_swissadme_data(ingredient_data)

        # ✅ JSON 저장 (subdir="raw" 설정 유지)
        save_to_json(results, output_file)
        print(f"✅ {herb_name} 크롤링 완료! 저장됨: {output_file}")

    else:
        print(f"❌ {herb_name}에 유효한 SMILES 값이 없습니다.")

if __name__ == "__main__":
    herb_names = ["고삼", "지모", "지황", "치자", "황금", "황련", "황백"]  # ✅ 여러 개의 약재 설정

    for herb in herb_names:
        save_swissadme_results(herb)  # ✅ 함수 내부에서 파일 로드 및 처리
