import time
import json
from tqdm import tqdm
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from modules.data_utils import get_driver  # ✅ WebDriver 설정 불러오기

SWISSADME_URL = "http://www.swissadme.ch/"

def safe_get_url(driver, url, max_retries=3):
    """안전하게 URL을 로드하는 함수 (타임아웃 발생 시 WebDriver 재시작)"""
    retries = 0
    while retries < max_retries:
        try:
            driver.get(url)
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
            return driver
        except Exception as e:
            print(f"⚠️ URL 로드 실패 ({retries + 1}/{max_retries}): {e}")
            retries += 1
            driver.quit()
            time.sleep(2)
            driver = get_driver()

    print(f"❌ {url} 로드 실패. 크롤링 건너뜀")
    return None

def get_swissadme_data(ingredient_data):
    """SwissADME에서 모든 분자적 속성을 크롤링"""
    driver = get_driver()  # ✅ WebDriver 실행
    driver = safe_get_url(driver, SWISSADME_URL)  # ✅ 안전한 URL 로드

    results = []

    for ingredient in tqdm(ingredient_data, desc="🚀 SwissADME 크롤링 중"):
        smiles = ingredient["molecule_smile"]
        
        # ✅ 기존 데이터 유지
        ingredient_info = {**ingredient, "swissadme_results": {}}

        if smiles in ["Not Available", "not found", ""]:
            print(f"⚠️ SMILES 값 없음: {ingredient['ingredient_name']} → SwissADME 크롤링 생략")
            results.append(ingredient_info)  # ✅ SMILES 없더라도 기존 데이터 유지하여 저장
            continue  

        try:
            # ✅ SMILES 입력 필드 찾기 및 입력
            smiles_input = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "smiles"))
            )
            smiles_input.clear()
            smiles_input.send_keys(smiles)

            # ✅ 실행 버튼 클릭
            run_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.ID, "submitButton"))
            )
            run_button.click()

            # ✅ 결과 로딩 대기 (최대 10초)
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//tr"))
            )

            # ✅ SwissADME 결과 저장
            table_rows = driver.find_elements(By.XPATH, "//tr")
            swissadme_results = {}

            for row in table_rows:
                try:
                    cells = row.find_elements(By.TAG_NAME, "td")
                    if len(cells) == 2:
                        key = cells[0].text.strip()
                        value = cells[1].text.strip()
                        swissadme_results[key] = value
                except Exception:
                    continue

            ingredient_info["swissadme_results"] = swissadme_results
            results.append(ingredient_info)

        except Exception as e:
            print(f"❌ SMILES {smiles} 처리 중 오류 발생: {e}")

            # ✅ WebDriver가 멈춘 경우 재시작
            driver.quit()
            time.sleep(2)
            driver = get_driver()
            driver = safe_get_url(driver, SWISSADME_URL)

    driver.quit()
    return results
