# modules/utils/crawling_utils.py

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests
from .web_driver import get_driver
from .logger import setup_logger
from config.settings import API_TIMEOUT

logger = setup_logger("crawling_utils")


def fetch_with_selenium(url: str, selector: str, attribute: str = "text", timeout: int = 10):
    """🕷️ Selenium을 사용한 크롤링"""
    driver = get_driver()
    if not driver:
        logger.error("❌ WebDriver 초기화 실패")
        return []

    logger.info(f"🌐 URL 요청 중: {url}")
    try:
        driver.get(url)
        WebDriverWait(driver, timeout).until(EC.presence_of_element_located((By.CSS_SELECTOR, selector)))
        elements = driver.find_elements(By.CSS_SELECTOR, selector)
        data = [e.get_attribute("href") if attribute == "href" else e.text for e in elements]
        logger.info(f"✅ 크롤링 완료: {len(data)}개 항목")
        return data
    except Exception as e:
        logger.error(f"❌ 크롤링 실패: {e}")
        return []
    finally:
        driver.quit()


def fetch_with_api(url: str, params: dict = None, method: str = "GET", timeout: int = API_TIMEOUT):
    """🔗 API 요청"""
    logger.info(f"🔗 API 요청 중: {url} | 파라미터: {params}")
    try:
        response = requests.request(method, url, params=params, timeout=timeout)
        response.raise_for_status()
        logger.info("✅ API 요청 성공")
        return response.json()
    except requests.RequestException as e:
        logger.error(f"❌ API 요청 실패: {e}")
        return None
