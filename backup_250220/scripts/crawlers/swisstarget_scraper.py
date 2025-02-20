import json
import sys
from modules.swisstarget_utils import get_swisstarget_data
from modules.data_utils import load_from_json, save_to_json

def main():
    """SwissTargetPrediction 크롤링 실행"""
    input_file = "herb_ingredients_test.json"  # 입력 파일명
    output_file = "swiss_target_results.json"  # 결과 저장 파일명

    print(f"🚀 SwissTargetPrediction 크롤링 시작")
    
    # ✅ JSON 데이터 로드
    herb_data = load_from_json(input_file, subdir="raw")
    if not herb_data:
        print(f"❌ {input_file} 데이터 로드 실패")
        sys.exit(1)

    # ✅ SwissTargetPrediction 실행
    results = get_swisstarget_data(herb_data)

    if results:
        save_to_json(results, output_file, subdir="processed")
        print(f"✅ 크롤링 완료! 결과 저장: {output_file}")
    else:
        print("❌ 크롤링된 데이터가 없습니다.")

if __name__ == "__main__":
    main()
