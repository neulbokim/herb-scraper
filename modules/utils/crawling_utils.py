from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time

def fetch_with_selenium(url, css_selector, max_retries=3, attribute="text"):
    """
    📝 Selenium을 사용해 웹 페이지에서 데이터를 가져오는 함수
    Args:
        url (str): 크롤링할 URL
        css_selector (str): 찾을 CSS 선택자
        max_retries (int): 최대 재시도 횟수
        attribute (str): 추출할 HTML 속성 (기본: 텍스트)
    """
    retries = 0
    while retries < max_retries:
        try:
            # Selenium WebDriver 설정
            options = Options()
            options.add_argument("--headless")
            driver = webdriver.Chrome(options=options)
            driver.get(url)
            
            # 기다리기
            time.sleep(5)  # 페이지 로딩 시간 기다리기 (적절히 조정 필요)

            # 데이터를 찾고 추출
            elements = driver.find_elements(By.CSS_SELECTOR, css_selector)
            if attribute == "href":
                return [el.get_attribute("href") for el in elements]
            else:
                return [el.text for el in elements]
        
        except Exception as e:
            print(f"Error: {e}, retrying...")
            retries += 1
            time.sleep(3)  # 재시도 대기 시간
        
        finally:
            driver.quit()
    
    return None
