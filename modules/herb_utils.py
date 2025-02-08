from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import time
import os
import json
from tqdm import tqdm
from modules.data_utils import get_driver, save_to_json  # ✅ WebDriver 및 JSON 저장 함수 가져옴

BASE_URL = "http://herb.ac.cn"


def safe_get_url(driver, url, max_retries=3):
    """안전하게 URL을 로드하는 함수 (타임아웃 발생 시 WebDriver 재시작)"""
    retries = 0
    while retries < max_retries:
        try:
            driver.get(url)
            
            # ✅ 불필요한 리소스가 로드되기 전에 HTML 요소만 빠르게 로드
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "body")))
            return driver
        
        except Exception as e:
            print(f"⚠️ URL 로드 실패 ({retries + 1}/{max_retries}): {e}")
            retries += 1
            
            driver.quit()
            time.sleep(2)
            driver = get_driver()

    print(f"❌ {url} 로드 실패. 크롤링 건너뜀")
    return None


def set_items_per_page(driver):
    """페이지에서 50개씩 표시되도록 설정"""
    try:
        dropdown = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CLASS_NAME, "ant-pagination-options-size-changer"))
        )
        
        # JavaScript를 이용해 드롭다운 메뉴 클릭
        driver.execute_script("arguments[0].click();", dropdown)
        time.sleep(1)

        option_50 = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//li[contains(text(), '50 / page')]"))
        )
        
        # JavaScript로 50개 옵션 클릭
        driver.execute_script("arguments[0].click();", option_50)
        time.sleep(2)

        WebDriverWait(driver, 5).until(
            EC.text_to_be_present_in_element((By.CLASS_NAME, "ant-pagination-options-size-changer"), "50 / page")
        )
        print("✅ 한 페이지에 50개씩 표시되도록 설정 완료!")
    except Exception as e:
        print(f"⚠️ 페이지 크기 변경 실패: {e}")



def extract_ingredient_details(driver):
    """각 성분 페이지에서 PubChem ID, CAS ID 등 주요 ID 정보를 가져옴"""
    ingredient_details = {}

    try:
        # ✅ ID 정보가 포함된 리스트 아이템 가져오기
        id_elements = WebDriverWait(driver, 5).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, "ant-list-item"))
        )

        for element in id_elements:
            try:
                key_element = element.find_element(By.TAG_NAME, "b")
                value_element = element.find_element(By.TAG_NAME, "a")  # 링크 포함된 경우
                key = key_element.text.strip()
                
                # ✅ 툴팁 여부 확인 후 가져오기
                try:
                    tooltip_element = element.find_element(By.XPATH, ".//span[contains(@class, 'ant-tooltip')]")
                    ActionChains(driver).move_to_element(tooltip_element).perform()
                    time.sleep(1)  # 툴팁이 나타날 시간을 줌

                    value = tooltip_element.text.strip()
                except Exception:
                    value = value_element.text.strip() if value_element else element.text.split(":")[-1].strip()

                # ✅ ID 정보 저장
                ingredient_details[key] = value
            except Exception:
                continue

    except Exception as e:
        print(f"⚠️ ID 정보 추출 실패: {e}")

    return ingredient_details



def get_all_ingredient_links(base_url):
    """'Related Ingredients' 테이블의 성분 링크만 가져옴"""
    all_links = set()
    page = 1
    driver = get_driver()
    driver.get(base_url)
    time.sleep(3)

    # ✅ 먼저 50개씩 표시 설정 (한 번 적용했지만, 다시 적용 필요)
    set_items_per_page(driver)
    
    while True:
        print(f"📄 페이지 {page} 크롤링 중... (Related Ingredients)")

        try:
            # ✅ "Related Ingredients" 테이블 찾기
            related_table = None
            headers = driver.find_elements(By.CLASS_NAME, "ant-typography")

            for header in headers:
                if header.text.strip() == "Related Ingredients":
                    try:
                        parent_div = header.find_element(By.XPATH, "./following-sibling::div[1]")
                        related_table = parent_div.find_element(By.CLASS_NAME, "ant-table-wrapper")
                        print("✅ 정확한 'Related Ingredients' 테이블 찾음!")
                        break
                    except Exception:
                        print("⚠️ 'Related Ingredients' 테이블을 찾을 수 없음.")

            if not related_table:
                print("❌ 'Related Ingredients' 테이블을 찾을 수 없습니다. 크롤링 종료.")
                break

            # ✅ Related Ingredients의 페이지네이션을 찾고, 다시 50개씩 표시하도록 설정
            try:
                pagination = related_table.find_element(By.XPATH, ".//ul[contains(@class, 'ant-pagination')]")
                size_changer = pagination.find_element(By.XPATH, ".//div[contains(@class, 'ant-pagination-options-size-changer')]")

                # ✅ JavaScript로 드롭다운 클릭 (50개 선택)
                driver.execute_script("arguments[0].click();", size_changer)
                time.sleep(1)

                option_50 = pagination.find_element(By.XPATH, ".//li[contains(text(), '50 / page')]")
                driver.execute_script("arguments[0].click();", option_50)
                time.sleep(3)

                print("✅ 'Related Ingredients' 페이지 크기 50개로 변경 완료!")

            except Exception as e:
                print(f"⚠️ 'Related Ingredients' 페이지 크기 변경 실패: {e}")

            # ✅ 현재 페이지 번호 확인
            try:
                current_page_element = related_table.find_element(By.XPATH, ".//ul[contains(@class, 'ant-pagination')]//li[contains(@class, 'ant-pagination-item-active')]")
                current_page = int(current_page_element.text.strip())
                print(f"🔍 현재 'Related Ingredients' 페이지: {current_page}")

            except Exception as e:
                print(f"⚠️ 'Related Ingredients' 페이지 번호 확인 실패: {e}")
                break

            # ✅ 현재 테이블의 기존 행 데이터 저장
            old_rows = related_table.find_elements(By.XPATH, ".//tbody/tr")
            old_row_texts = [row.text for row in old_rows]

            print(f"🔍 현재 페이지에서 {len(old_rows)}개의 관련 성분을 찾았습니다.")

            for row in old_rows:
                try:
                    link_element = row.find_element(By.XPATH, ".//td[1]/span/a")
                    if link_element:
                        href = link_element.get_attribute("href")

                        # ✅ URL 중복 문제 해결
                        if href.startswith("http"):
                            full_url = href
                        else:
                            full_url = BASE_URL + href

                        if "/Detail/?v=HBIN" in full_url:
                            all_links.add(full_url)
                            print(f"   ✅ Related Ingredient 링크 추가됨: {full_url}")
                except Exception:
                    print("⚠️ 일부 행에서 링크를 찾을 수 없음.")

            # ✅ "Related Ingredients"의 **올바른 페이지네이션 찾기**
            try:
                pagination = related_table.find_element(By.XPATH, ".//ul[contains(@class, 'ant-pagination')]")
                next_page_button = pagination.find_element(By.XPATH, ".//li[@title='Next Page']")

                if "ant-pagination-disabled" in next_page_button.get_attribute("class"):
                    print(f"🚫 마지막 페이지({page}) 도달. 크롤링 종료.")
                    break  # ✅ 마지막 페이지면 종료

                # ✅ JavaScript로 강제 클릭
                driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", next_page_button)
                driver.execute_script("arguments[0].click();", next_page_button)
                time.sleep(3)

                # ✅ **새로운 테이블 데이터가 로드될 때까지 대기**
                attempts = 0
                while attempts < 10:  # 최대 10번(20초) 재시도
                    new_page_element = related_table.find_element(By.XPATH, ".//ul[contains(@class, 'ant-pagination')]//li[contains(@class, 'ant-pagination-item-active')]")
                    new_page = int(new_page_element.text.strip())

                    if new_page > current_page:
                        print(f"✅ 'Related Ingredients' 페이지 변경됨: {current_page} → {new_page}")
                        break

                    time.sleep(2)
                    attempts += 1

                if attempts == 10:
                    print("⚠️ 새로운 페이지 데이터 로드 실패. 크롤링 중단.")
                    break

                page += 1  # ✅ 페이지 번호 증가

            except Exception as e:
                print(f"⚠️ 'Related Ingredients' 다음 페이지 버튼 클릭 실패: {e}")
                break  # ✅ 다음 페이지 버튼이 없거나 오류 발생하면 종료

        except Exception as e:
            print(f"⚠️ 'Related Ingredients' 크롤링 중 오류 발생: {e}")
            break

    driver.quit()
    return list(all_links)


def extract_molecule_data(driver):
    """Ingredient 페이지에서 Molecule SMILE과 Ingredient Name 추출"""
    molecule_smile = "not found"
    ingredient_name = "N/A"

    try:
        # ✅ Ingredient Name 가져오기 (최대 10초 대기)
        name_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//b[contains(text(), 'Ingredient name')]/following-sibling::span"))
        )
        ingredient_name = name_element.get_attribute("textContent").strip()

        # ✅ 잘려 있는 경우 툴팁에서 가져오기
        if "..." in ingredient_name:
            print("⚠️ Ingredient Name이 잘려 있음 → 툴팁에서 가져오기 시도")

            # ✅ 마우스 Hover 후 기다리기
            ActionChains(driver).move_to_element(name_element).perform()
            time.sleep(2)  # 툴팁 활성화 대기

            # ✅ ant-tooltip 요소 확인 후 가져오기
            WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.CLASS_NAME, "ant-tooltip-inner"))
            )
            tooltips = driver.find_elements(By.CLASS_NAME, "ant-tooltip-inner")

            if tooltips:
                ingredient_name = tooltips[-1].text.strip()  # ✅ 마지막 툴팁 가져오기 (가장 최근 것)

        print(f"✅ Ingredient Name: {ingredient_name}")

    except Exception as e:
        print(f"⚠️ Ingredient Name 추출 실패: {e}")

    try:
        # ✅ Molecule SMILE 가져오기 (최대 5초 대기)
        smile_element = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.XPATH, "//b[contains(text(), 'Molecule smile')]/following-sibling::span"))
        )
        molecule_smile = smile_element.get_attribute("textContent").strip()

        # ✅ 잘려 있는 경우 툴팁에서 가져오기
        if "..." in molecule_smile:
            print("⚠️ SMILES 값이 잘려 있음 → 툴팁에서 가져오기 시도")

            # ✅ 마우스 Hover 후 기다리기
            ActionChains(driver).move_to_element(smile_element).perform()
            time.sleep(2)  # 툴팁 활성화 대기

            # ✅ ant-tooltip 요소 확인 후 가져오기
            WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.CLASS_NAME, "ant-tooltip-inner"))
            )
            tooltips = driver.find_elements(By.CLASS_NAME, "ant-tooltip-inner")

            if tooltips:
                molecule_smile = tooltips[-1].text.strip()  # ✅ 마지막 툴팁 가져오기

        print(f"✅ Molecule SMILE: {molecule_smile}")

    except Exception:
        print(f"⚠️ SMILES 요소를 찾을 수 없음 → 'not found'로 설정")

    return ingredient_name, molecule_smile


def scrape_herb_ingredients(herb_name, herb_url):
    """한 개의 한약재에 대한 활성 성분 크롤링"""
    print(f"🌿 {herb_name} 크롤링 시작: {herb_url}")

    driver = get_driver()
    driver.get(herb_url)
    time.sleep(3)

    ingredient_links = get_all_ingredient_links(herb_url)
    driver.quit()

    if not ingredient_links:
        print(f"⚠️ {herb_name}에서 성분 링크를 찾을 수 없음.")
        return None

    herb_data = {}
    for link in ingredient_links:
        print(f"   → 성분 크롤링: {link}")
        driver = get_driver()
        driver.get(link)
        time.sleep(3)

        ingredient_name, molecule_smile = extract_molecule_data(driver)
        id_details = extract_ingredient_details(driver)  # ✅ ID 정보 가져오기
        driver.quit()

        herb_data[link] = {
            "ingredient_name": ingredient_name,
            "molecule_smile": molecule_smile,
            **id_details  # ✅ ID 정보 추가
        }

    return herb_data if herb_data else None


def save_herb_ingredients(herb_name, herb_url):
    """한 개의 한약재에 대한 성분 크롤링 및 저장"""
    output_file = f"data/raw/herb_ingredients_{herb_name}.json"
    os.makedirs(os.path.dirname(output_file), exist_ok=True)

    herb_data = scrape_herb_ingredients(herb_name, herb_url)

    if herb_data:
        save_to_json(herb_data, output_file)
        print(f"✅ 크롤링 완료! 결과가 {output_file} 파일에 저장되었습니다.")
    else:
        print(f"❌ {herb_name} 크롤링 실패.")
