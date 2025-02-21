# modules/data_utils.py

import os
import json
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

DATA_DIR = "data"  # ✅ 데이터 저장 기본 디렉토리
RAW_DIR = os.path.join(DATA_DIR, "raw")  # ✅ 기본적으로 raw 디렉토리 사용
PROCESSED_DIR = os.path.join(DATA_DIR, "processed")  # ✅ CSV 저장을 위한 processed 디렉토리

def save_to_json(data, filename, subdir=None, verbose=True):
    """JSON 파일을 지정된 서브디렉토리에 저장 (기본: data/raw)"""
    if subdir:
        save_path = os.path.join(DATA_DIR, subdir, filename)
    else:
        save_path = os.path.join(RAW_DIR, filename)  # ✅ 기본적으로 data/raw 사용

    os.makedirs(os.path.dirname(save_path), exist_ok=True)  # ✅ 디렉토리 생성
    with open(save_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

    if verbose:
        print(f"📁 JSON 데이터 저장 완료: {save_path}")

def save_to_csv(data, filename, subdir=None, verbose=True):
    """CSV 파일을 지정된 서브디렉토리에 저장 (기본: data/processed)"""
    if subdir:
        save_path = os.path.join(DATA_DIR, subdir, filename)
    else:
        save_path = os.path.join(PROCESSED_DIR, filename)  # ✅ 기본적으로 data/processed 사용

    os.makedirs(os.path.dirname(save_path), exist_ok=True)  # ✅ 디렉토리 생성
    df = pd.DataFrame(data)
    df.to_csv(save_path, index=False, encoding="utf-8-sig")

    if verbose:
        print(f"📁 CSV 데이터 저장 완료: {save_path}")
        
def save_to_excel(data, filename, subdir=None, verbose=True):
    """Excel 파일을 지정된 서브디렉토리에 저장 (기본: data/processed)"""
    if subdir:
        save_path = os.path.join(DATA_DIR, subdir, filename)
    else:
        save_path = os.path.join(PROCESSED_DIR, filename)  # 기본적으로 data/processed 사용

    os.makedirs(os.path.dirname(save_path), exist_ok=True)  # 디렉토리 생성
    df = pd.DataFrame(data)
    df.to_excel(save_path, index=False, engine="xlsxwriter")

    if verbose:
        print(f"📁 Excel 데이터 저장 완료: {save_path}")
        

def load_from_json(filename, subdir="raw", verbose=True):
    """JSON 파일 불러오기 (기본: data/raw 디렉토리)"""
    file_path = os.path.join(DATA_DIR, subdir, filename)

    if not os.path.exists(file_path):
        if verbose:
            print(f"⚠️ 파일 없음: {file_path}")
        return {}

    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)

def get_driver():
    """불필요한 리소스 차단한 Selenium WebDriver 설정"""
    options = Options()
    options.headless = False  # ✅ True로 설정하면 브라우저 창 없이 실행 가능
    #options.add_argument("--incognito")  # 시크릿 모드 사용
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36")

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)


    # ✅ Chrome DevTools Protocol(CDP)로 이미지, CSS, JS 차단
    #driver.execute_cdp_cmd("Network.setBlockedURLs", {
    #   "urls": ["*.jpg", "*.png", "*.gif", "*.css", "*.woff", "*.woff2", "*.ttf", "*.svg"]
    #})
    driver.execute_cdp_cmd("Network.setBlockedURLs", {"urls": ["*.jpg", "*.png", "*.gif"]})
    driver.execute_cdp_cmd("Network.enable", {})

    return driver

def safe_get_url(driver, url, max_retries=3):
    """
    ✅ 안전하게 URL 로드 (로딩 실패 시 driver 재시작)
    """
    retries = 0
    while retries < max_retries:
        try:
            driver.get(url)
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
            print(f"✅ URL 로드 성공: {url}")
            return driver
        except Exception as e:
            retries += 1
            print(f"⚠️ URL 로드 실패 ({retries}/{max_retries}): {e}")
            driver.quit()
            print("🔄 ChromeDriver 재시작 중...")
            time.sleep(2)
            driver = get_driver()
    print(f"❌ {url} 최대 재시도 실패 - 크롤링 건너뜀")
    return None