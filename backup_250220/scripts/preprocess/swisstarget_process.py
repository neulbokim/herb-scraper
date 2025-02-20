from modules.data_utils import load_from_json, save_to_json

def process_swisstarget_data():
    """SwissTargetPrediction 크롤링 데이터 정리"""
    input_file = "swiss_target_prediction.json"
    output_file = "swiss_target_final.json"

    raw_data = load_from_json(input_file, subdir="processed")

    processed_data = []

    for item in raw_data:
        herb_name = item.get("herb_name", "Unknown")
        ingredient_name = item.get("ingredient_name", "Unknown")
        molecule_smile = item.get("molecule_smile", "Unknown")

        for target in item.get("swiss_target_results", []):
            processed_data.append({
                "Herb": herb_name,
                "Ingredient": ingredient_name,
                "Molecule SMILE": molecule_smile,
                **target
            })

    save_to_json(processed_data, output_file, subdir="processed")
    print(f"✅ 최종 데이터 저장 완료: {output_file}")

if __name__ == "__main__":
    process_swisstarget_data()
