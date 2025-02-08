import pandas as pd
from modules.data_utils import load_from_json, save_to_json

def merge_data():
    """HERB, SwissADME, BATMAN-TCM 데이터를 통합"""

    # 데이터 로드
    herb_data = load_from_json("herb_ingredients.json")
    swissadme_data = load_from_json("swissadme_filtered.json")
    batman_tcm_data = load_from_json("batman_tcm_results.json")

    final_data = []

    # SwissADME 데이터를 딕셔너리 형태로 변환 (빠른 조회를 위해)
    swissadme_dict = {item["molecule_smile"]: item for item in swissadme_data}

    # BATMAN-TCM 데이터를 딕셔너리 형태로 변환
    batman_tcm_dict = {smiles: targets for smiles, targets in batman_tcm_data.items()}

    # 데이터 병합
    for herb_name, ingredients in herb_data.items():
        for ingredient in ingredients:
            smiles = ingredient.get("molecule_smile")
            swissadme_info = swissadme_dict.get(smiles, {})
            batman_targets = batman_tcm_dict.get(smiles, [])

            final_data.append({
                "herb": herb_name,
                "ingredient_id": ingredient.get("ingredient_url").split("=")[-1].split("&")[0],  # ID 추출
                "molecule_smile": smiles,
                "TPSA": swissadme_info.get("TPSA", None),
                "Lipinski": swissadme_info.get("Lipinski", None),
                "Bioavailability": swissadme_info.get("Bioavailability", None),
                "target_proteins": ", ".join(batman_targets)
            })

    # 데이터프레임으로 변환
    df = pd.DataFrame(final_data)

    # CSV로 저장
    df.to_csv("../data/processed/final_dataset.csv", index=False, encoding="utf-8")
    print("✅ 최종 데이터 저장 완료: data/processed/final_dataset.csv")