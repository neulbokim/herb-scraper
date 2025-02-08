from modules.data_utils import save_to_json, load_from_json, get_driver
from modules.herb_utils import extract_molecule_data, extract_ingredient_details, safe_get_url
import time
import os

INPUT_FILE = "herb_ingredient_urls.json" # ✅ 단일 JSON 파일 사용
OUTPUT_DIR = "data/raw"  # ✅ 출력 데이터 폴더


def scrape_ingredient_details():
    """모든 한약재의 성분 상세 정보를 크롤링하여 저장"""

    # ✅ 단일 JSON 파일에서 모든 한약재 데이터를 불러옴
    if not os.path.exists(os.path.join(OUTPUT_DIR, INPUT_FILE)):
        print("❌ 성분 URL 데이터가 없습니다. 먼저 `herb_scraper.py`를 실행하세요!")
        return

    herb_data = load_from_json(INPUT_FILE)

    for herb_name, ingredient_urls in herb_data.items():  # ✅ 각 약재별로 크롤링 수행
        output_file = f"herb_ingredients_{herb_name}.json"

        if not ingredient_urls:
            print(f"⚠️ {herb_name}의 성분 URL 데이터가 비어 있습니다. 건너뜀.")
            continue

        print(f"\n🌿 {herb_name} 성분 상세 크롤링 시작...")
        all_ingredient_data = {}

        driver = get_driver()  # ✅ WebDriver 실행

        for idx, url in enumerate(ingredient_urls):
            print(f"   → [{idx+1}/{len(ingredient_urls)}] 성분 페이지 크롤링: {url}")
            time.sleep(1)  # 부하 방지

            # ✅ 안전하게 URL 로드 (타임아웃 발생 시 WebDriver 재시작)
            driver = safe_get_url(driver, url)
            if driver is None:
                print(f"❌ {url} 크롤링 실패, 건너뜀")
                continue

            try:
                # ✅ 데이터 추출
                ingredient_name, molecule_smile = extract_molecule_data(driver)
                id_details = extract_ingredient_details(driver)  # ✅ 추가적인 ID 정보 가져오기

                # ✅ 데이터 저장
                all_ingredient_data[url] = {
                    "ingredient_name": ingredient_name,
                    "molecule_smile": molecule_smile,
                    **id_details  # ✅ PubChem ID, CAS ID 등 추가
                }

            except Exception as e:
                print(f"⚠️ 데이터 추출 중 오류 발생: {e}")
                continue  # ✅ 오류 발생 시 해당 URL만 건너뜀

        driver.quit()  # WebDriver 종료

        # ✅ 한약재별 JSON 파일 저장
        save_to_json(all_ingredient_data, output_file)
        print(f"📁 {herb_name} 데이터 저장 완료: {output_file}")



if __name__ == "__main__":
    scrape_ingredient_details()
