import os
import json
import time
from tqdm import tqdm
from modules.data_utils import load_from_json, save_to_json
from modules.swissadme_utils import get_swissadme_data  # ✅ SwissADME 크롤링 함수 가져오기

def find_missing_data(swissadme_data):
    """SwissADME 결과 중 SMILES와 Formula가 모두 빈 값인 데이터를 찾아서 다시 크롤링할 리스트 생성"""
    missing_data = []

    for entry in swissadme_data:
        swissadme_results = entry.get("swissadme_results", {})

        # ✅ SMILES와 Formula가 모두 비어있는 경우만 재검색 대상
        if (
            "SMILES" in swissadme_results and "Formula" in swissadme_results and
            swissadme_results["SMILES"] == "" and swissadme_results["Formula"] == ""
        ):
            missing_data.append(entry)

    return missing_data


def refill_swissadme_data(herb_name):
    """SwissADME 결과에서 부족한 데이터를 찾아서 다시 크롤링 후 업데이트"""
    input_swissadme_file = f"swissadme_results_{herb_name}.json"
    input_herb_file = f"herb_ingredients_{herb_name}.json"
    
    # ✅ JSON 파일 로드
    if not os.path.exists(os.path.join("data/raw", input_swissadme_file)):
        print(f"❌ {input_swissadme_file} 파일이 없습니다. 크롤링을 먼저 실행하세요.")
        return

    if not os.path.exists(os.path.join("data/raw", input_herb_file)):
        print(f"❌ {input_herb_file} 파일이 없습니다. 원본 데이터를 찾을 수 없습니다.")
        return

    swissadme_data = load_from_json(input_swissadme_file)
    herb_data = load_from_json(input_herb_file)

    # ✅ 비어 있는 데이터 찾기
    missing_entries = find_missing_data(swissadme_data)

    if not missing_entries:
        print(f"✅ {herb_name}의 SwissADME 데이터는 모두 채워져 있습니다.")
        return

    print(f"🔍 {herb_name}의 {len(missing_entries)}개 성분에 대한 부족한 데이터를 다시 가져옵니다.")

    # ✅ 원본 데이터에서 ingredient_name 및 molecule_smile 가져오기
    for entry in missing_entries:
        url = entry["ingredient_url"]

        if url in herb_data:
            entry["ingredient_name"] = herb_data[url].get("ingredient_name", "N/A")
            entry["molecule_smile"] = herb_data[url].get("molecule_smile", "not found")

    # ✅ SwissADME 재검색 실행
    updated_results = get_swissadme_data(missing_entries)
    time.sleep(2.5)

    # ✅ 기존 데이터 업데이트 (기존 값 + 새롭게 가져온 값 병합)
    for original_entry, new_entry in zip(swissadme_data, updated_results):
        if new_entry["ingredient_url"] in [entry["ingredient_url"] for entry in missing_entries]:
            original_entry.update(new_entry)

    # ✅ JSON 파일 업데이트
    save_to_json(swissadme_data, input_swissadme_file)
    print(f"✅ {herb_name}의 SwissADME 데이터 업데이트 완료: {input_swissadme_file}")


if __name__ == "__main__":
    herb_names = ["고삼", "지모", "지황", "치자", "황금", "황련", "황백"]  # ✅ 여러 개의 약재 설정

    for herb in herb_names:
        refill_swissadme_data(herb)  # ✅ 부족한 데이터 보완 실행
