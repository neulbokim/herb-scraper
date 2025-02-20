import os
import json
import pandas as pd
from modules.data_utils import load_from_json, save_to_csv

DATA_DIR = "data/tcmsp"  # ✅ 변환할 데이터가 저장된 폴더
HERBS = ["황금", "황련", "치자", "황백"]  # ✅ 변환할 약재 목록

def convert_json_to_csv(herb_name):
    """저장된 tcmsp_{herb_name}.json을 읽어 성분 및 타겟 정보를 분리하여 CSV로 저장"""
    json_filename = f"tcmsp_{herb_name}.json"
    json_path = os.path.join(DATA_DIR, json_filename)

    if not os.path.exists(json_path):
        print(f"⚠️ {json_path} 파일이 존재하지 않습니다.")
        return

    print(f"🔄 {json_filename} → CSV 변환 중...")

    # ✅ JSON 데이터 로드
    data = load_from_json(json_filename, "tcmsp")
    ingredients = []
    targets = []

    # ✅ JSON 데이터 변환 (성분 + 타겟 개별 행)
    for entry in data:
        mol_id = entry["mol_id"]
        mol_name = entry["mol_name"]
        mol_url = entry["mol_url"]
        mw = entry["mw"]
        alogp = entry["alogp"]
        hdon = entry["hdon"]
        hacc = entry["hacc"]
        ob = entry["ob"]
        caco2 = entry["caco2"]
        bbb = entry["bbb"]
        dl = entry["dl"]
        fasa = entry["fasa"]
        halflife = entry["halflife"]
        
        # ✅ 성분 정보 저장
        ingredients.append({
            "mol_id": mol_id,
            "mol_name": mol_name,
            "mol_url": mol_url,
            "mw": mw,
            "alogp": alogp,
            "hdon": hdon,
            "hacc": hacc,
            "ob": ob,
            "caco2": caco2,
            "bbb": bbb,
            "dl": dl,
            "fasa": fasa,
            "halflife": halflife
        })

        # ✅ 타겟 정보 저장 (각 타겟별 개별 행)
        for target in entry.get("targets", []):
            targets.append({
                "mol_id": mol_id,
                "mol_name": mol_name,
                "mol_url": mol_url,
                "target_name": target["target_name"],
                "target_id": target["target_id"],
                "drugbank_id": target["drugbank_id"]
            })

    # ✅ CSV 파일 저장
    save_to_csv(ingredients, f"tcmsp_{herb_name}_ingredients.csv", "tcmsp")
    save_to_csv(targets, f"tcmsp_{herb_name}_targets.csv", "tcmsp")

    print(f"✅ {herb_name} 변환 완료!")

if __name__ == "__main__":
    for herb in HERBS:
        convert_json_to_csv(herb)

    print("🎉 모든 변환 완료!")
