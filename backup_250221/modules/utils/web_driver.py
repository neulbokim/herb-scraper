# modules/utils/web_driver.py

import chromedriver_autoinstaller
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from modules.utils.logger import setup_logger

logger = setup_logger("web_driver")

def get_driver(headless=False):
    """🌐 Chrome WebDriver 생성 및 설정"""
    try:
        # ✅ ChromeDriver 자동 설치 및 경로 설정
        chromedriver_autoinstaller.install()

        options = Options()
        if headless:
            options.add_argument("--headless")
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")

        service = Service()
        driver = webdriver.Chrome(service=service, options=options)
        logger.info("✅ WebDriver 생성 완료")
        return driver

    except Exception as e:
        logger.error(f"❌ WebDriver 생성 실패: {e}")
        return None

