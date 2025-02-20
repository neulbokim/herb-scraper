# modules/utils/web_driver.py

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from modules.utils.logger import setup_logger

logger = setup_logger("web_driver")

def get_driver(headless: bool = True):
    """🌐 Selenium WebDriver 설정"""
    try:
        options = webdriver.ChromeOptions()
        if headless:
            options.add_argument("--headless")
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        logger.info("✅ WebDriver 생성 완료")
        return driver
    except Exception as e:
        logger.error(f"❌ WebDriver 생성 실패: {e}")
        return None
