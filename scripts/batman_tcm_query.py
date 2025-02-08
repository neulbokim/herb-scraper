import os
import json
from modules.batman_tcm_utils import get_target_proteins
from modules.data_utils import load_from_json, save_to_json

PROCESSED_DIR = "data/raw"
OUTPUT_DIR = "data/processed"

def run_batman_tcm(herb_name):
    """SwissADME 데이터에서 PubChem ID 값을 가져와 BATMAN-TCM 실행"""
    
    input_file = f"swissadme_results_{herb_name}.json"
    output_file = f"batman_tcm_results_{herb_name}.json"

    # ✅ SwissADME 데이터 로드
    if not os.path.exists(os.path.join(PROCESSED_DIR, input_file)):
        print(f"❌ {os.path.join(PROCESSED_DIR, input_file)} 파일이 없습니다. 먼저 SwissADME 크롤링을 실행하세요.")
        return

    swissadme_data = load_from_json(input_file)

    # ✅ PubChem ID 리스트 추출 (빈 값 포함)
    pubchem_list = []
    ingredient_map = {}  # ✅ PubChem ID를 key로 한약재 정보를 저장

    for entry in swissadme_data:
        pubchem_id = entry.get("PubChem id", "").strip()

        # ✅ PubChem ID가 있을 경우 저장
        if pubchem_id and pubchem_id not in ["", "Not Available"]:
            pubchem_list.append(pubchem_id)

        # ✅ PubChem ID가 없어도 결과에 포함되도록 설정
        ingredient_map[pubchem_id] = {
            "ingredient_url": entry["ingredient_url"],
            "ingredient_name": entry["ingredient_name"],
            "PubChem id": pubchem_id if pubchem_id else "N/A",  # ✅ PubChem ID 없으면 "N/A"로 저장
            "batman_tcm_results": []  # ✅ 기본적으로 빈 리스트로 추가
        }

    # ✅ BATMAN-TCM API 호출
    if pubchem_list:
        print(f"🚀 {herb_name}의 BATMAN-TCM 분석 시작!")
        batman_tcm_results = get_target_proteins(pubchem_list)

        # ✅ API 결과 병합
        for pubchem_id, data in batman_tcm_results.items():
            if pubchem_id in ingredient_map:
                ingredient_map[pubchem_id]["batman_tcm_results"] = data  # ✅ 전체 결과 저장

    # ✅ JSON 파일 저장
    final_results = list(ingredient_map.values())  # ✅ 모든 데이터를 리스트로 변환하여 저장
    save_to_json(final_results, output_file)

    print(f"✅ {herb_name} BATMAN-TCM 결과 저장 완료: {output_file}")


if __name__ == "__main__":
    herb_names = ["고삼", "지모", "지황", "치자", "황금", "황련", "황백"]  # ✅ 여러 개의 약재 설정

    for herb in herb_names:
        run_batman_tcm(herb)  # ✅ BATMAN-TCM 분석 실행
