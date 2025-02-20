import os
import json
import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# 파일 경로 설정
CSV_FILE = "data/raw/active_ingredients_test.csv"
OUTPUT_FILE = "data/raw/stitch_results.json"

def create_driver():
    """새로운 WebDriver 세션을 생성하는 함수"""
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # GUI 없이 실행
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(options=options)
    return driver

def get_tnsf11_identifier(driver, active_ingredient):
    """
    STITCH에서 활성성분을 검색하고 TNSF11 Identifier를 추출하는 함수
    """
    try:
        # STITCH 검색 페이지 이동
        url = "http://stitch.embl.de/cgi/input.pl"
        driver.get(url)
        
        # 검색 입력란 찾기 (활성성분 입력)
        search_box = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.ID, "primary_input:single_identifier"))
        )
        search_box.clear()
        search_box.send_keys(active_ingredient)
        time.sleep(1)

        # Organism을 "Homo sapiens"로 설정
        organism_box = driver.find_element(By.ID, "species_text_single_identifier")
        organism_box.clear()
        organism_box.send_keys("Homo sapiens")
        time.sleep(1)

        # 'Search' 버튼 클릭
        search_button = driver.find_element(By.XPATH, "//a[contains(text(), 'Search')]")
        search_button.click()

        # 결과 페이지 로드 대기
        WebDriverWait(driver, 7).until(
            EC.presence_of_element_located((By.CLASS_NAME, "bottom_page_content_nav"))
        )

        # 'Legend' 탭 클릭
        legend_tab = driver.find_element(By.ID, "bottom_page_selector_legend")
        legend_tab.click()

        # TNFSF11이 있는지 확인하고 클릭
        try:
            tnsf11_element = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.XPATH, "//td[contains(text(), 'TNFSF11')]"))
            )
            tnsf11_element.click()

            # 팝업 창에서 Identifier 추출
            WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.ID, "fpWindowDiv"))
            )
            identifier_text = driver.find_element(By.XPATH, "//div[contains(text(), 'Identifier:')]").text
            identifier = identifier_text.split(":")[-1].strip()
            return identifier

        except Exception:
            return None  # TNFSF11이 없을 경우 None 반환

    except Exception as e:
        print(f"❌ 오류 발생 ({active_ingredient}): {e}")
        return None


def run_stitch_from_csv():
    """CSV에서 활성성분을 가져와 STITCH에서 검색"""
    if not os.path.exists(CSV_FILE):
        print(f"❌ CSV 파일이 없습니다: {CSV_FILE}")
        return

    df = pd.read_csv(CSV_FILE)
    required_columns = {"약재명", "활성성분"}
    if not required_columns.issubset(df.columns):
        print(f"❌ CSV 파일에 필요한 열({required_columns})이 없습니다.")
        return

    ingredient_map = {}  # 활성성분별 데이터 저장
    driver = create_driver()  # WebDriver 생성

    for _, row in df.iterrows():
        active_ingredient = str(row["활성성분"]).strip() if pd.notna(row["활성성분"]) else "N/A"

        # 검색할 활성성분이 있는 경우만 실행
        if active_ingredient not in ["", "N/A", "Not Available"]:
            identifier = get_tnsf11_identifier(driver, active_ingredient)

            # 만약 WebDriver 세션이 끊기면 다시 시작
            if identifier is None and "session deleted" in str(identifier):
                print("⚠️ WebDriver 세션이 종료됨. 다시 시작합니다...")
                driver.quit()
                driver = create_driver()
                identifier = get_tnsf11_identifier(driver, active_ingredient)

        else:
            identifier = None

        # 결과 저장
        ingredient_map[active_ingredient] = {
            "herb_name": row["약재명"],
            "ingredient_name": active_ingredient,
            "TNSF11 Identifier": identifier
        }

    driver.quit()  # WebDriver 종료

    # JSON 파일 저장
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(list(ingredient_map.values()), f, ensure_ascii=False, indent=4)

    print(f"✅ STITCH 결과 저장 완료: {OUTPUT_FILE}")


if __name__ == "__main__":
    run_stitch_from_csv()
