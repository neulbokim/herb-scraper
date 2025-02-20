import os
import time
import pandas as pd
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import UnexpectedAlertPresentException, NoAlertPresentException, TimeoutException
from modules.data_utils import get_driver

SWISSTARGET_URL = "http://www.swisstargetprediction.ch/index.php"
DOWNLOAD_PATH = "/Users/hyeonseokim_macbookpro/Downloads"  # 크롬의 기본 다운로드 폴더 설정

def safe_get_url(driver, url, max_retries=3):
    """SwissTargetPrediction 페이지 로드 (자동 Alert 처리 포함)"""
    retries = 0
    while retries < max_retries:
        try:
            driver.get(url)

            # ✅ Alert 감지 후 자동 해제
            try:
                WebDriverWait(driver, 3).until(EC.alert_is_present())
                alert = driver.switch_to.alert
                print(f"⚠️ Alert 감지됨: {alert.text}")
                alert.dismiss()  # Alert 창 닫기
                print("✅ Alert 닫기 완료")
            except NoAlertPresentException:
                pass  # Alert이 없으면 무시

            # ✅ 정상적으로 페이지가 로드될 때까지 대기
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )
            return driver

        except UnexpectedAlertPresentException:
            print("❌ Unexpected Alert 감지됨 → 닫기 시도")
            try:
                alert = driver.switch_to.alert
                alert.dismiss()
                print("✅ Alert 닫기 성공")
            except:
                pass  # Alert이 닫히지 않으면 무시
            
            retries += 1
            driver.quit()
            time.sleep(2)
            driver = get_driver()

    print(f"❌ {url} 로드 실패. 크롤링 건너뜀")
    return None

def get_latest_downloaded_file(download_path, extension=".csv"):
    """가장 최근에 다운로드된 CSV 파일 찾기"""
    files = [os.path.join(download_path, f) for f in os.listdir(download_path) if f.endswith(extension)]
    if not files:
        return None
    return max(files, key=os.path.getctime)  # 최신 파일 찾기

def extract_swisstarget_results_via_csv(driver):
    """SwissTargetPrediction에서 CSV 다운로드 후 데이터 추출"""
    try:
        # ✅ 결과 테이블 로드 대기
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "resultTable")))

        # ✅ CSV 다운로드 버튼 찾기 및 클릭
        csv_button = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.CLASS_NAME, "buttons-csv"))
        )
        print("✅ CSV 다운로드 버튼 찾음, 클릭 중...")
        ActionChains(driver).move_to_element(csv_button).click().perform()

        # ✅ 다운로드 완료 대기
        time.sleep(5)

        # ✅ 가장 최신 다운로드된 CSV 파일 가져오기
        csv_file = get_latest_downloaded_file(DOWNLOAD_PATH)
        if not csv_file:
            print("❌ CSV 파일 다운로드 실패")
            return []

        print(f"✅ CSV 파일 다운로드 완료: {csv_file}")

        # ✅ CSV 파일을 pandas로 읽어오기
        df = pd.read_csv(csv_file)
        print(f"✅ CSV 데이터 로드 완료: {df.shape[0]}개 행")

        # ✅ 필요한 정보 추출
        results = df.to_dict(orient="records")
        return results

    except Exception as e:
        print(f"⚠️ CSV 다운로드 및 데이터 추출 실패: {e}")
        return []

def get_swisstarget_data(herb_data):
    """SwissTargetPrediction 크롤링"""
    driver = get_driver()

    results = []

    for ingredient in herb_data:
        ingredient_name = ingredient.get("ingredient_name", "Unknown")
        smiles = ingredient.get("molecule_smile", "")

        if not smiles or smiles == "Not Available":
            print(f"⚠️ SMILES 값 없음: {ingredient_name} → SwissTargetPrediction 크롤링 생략")
            continue

        print(f"🚀 {ingredient_name}({smiles}) SwissTargetPrediction 실행 중...")

        try:
            # ✅ SwissTargetPrediction 초기 페이지 로드
            safe_get_url(driver, SWISSTARGET_URL)
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "smilesBox"))
            )
            print("✅ 초기 페이지 로드 완료")

            # ✅ SMILES 입력
            smiles_input = driver.find_element(By.ID, "smilesBox")
            smiles_input.clear()
            smiles_input.send_keys(smiles)

            # ✅ 클릭을 통해 포커스를 벗어나야 Predict 버튼 활성화됨
            driver.find_element(By.TAG_NAME, "body").click()
            time.sleep(2)

            # ✅ Predict 버튼 클릭
            predict_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.ID, "submitButton"))
            )
            predict_button.click()

            # ✅ 결과 페이지 로딩 대기
            WebDriverWait(driver, 30).until(
                EC.presence_of_element_located((By.ID, "resultTable"))
            )
            print("✅ 결과 페이지 로드 완료")

            # ✅ CSV 다운로드 방식으로 데이터 가져오기
            target_results = extract_swisstarget_results_via_csv(driver)

            results.append({
                "ingredient_name": ingredient_name,
                "molecule_smile": smiles,
                "swiss_target_results": target_results
            })

        except Exception as e:
            print(f"❌ SMILES {smiles} 처리 중 오류 발생: {e}")

    driver.quit()
    return results
