import os
import time
from bs4 import BeautifulSoup
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from modules.data_utils import get_driver

# ✅ TCMSP 데이터 저장 디렉토리 설정
TCMSP_DIR = "data/tcmsp"
os.makedirs(TCMSP_DIR, exist_ok=True)

class TCMSPScraper:
    BASE_URL = "https://tcmsp-e.com/tcmspsearch.php"
    MOLECULE_URL = "https://tcmsp-e.com/{path}"

    def __init__(self, herb_name, herb_url):
        self.herb_name = herb_name
        self.herb_url = herb_url
        self.driver = get_driver()
        self.driver.set_page_load_timeout(60)  # ✅ 페이지 로딩 타임아웃 60초 설정

    def get_total_pages(self):
        """총 페이지 수 계산 (숫자 페이지 링크만 추출)"""
        pagination_links = self.driver.find_elements(By.CSS_SELECTOR, ".k-pager-numbers .k-link")
        
        # ✅ "다음", "이전" 같은 비숫자 제거
        page_numbers = [
            int(link.get_attribute("data-page"))
            for link in pagination_links
            if link.get_attribute("data-page") and link.get_attribute("data-page").isdigit()
        ]

        total_pages = max(page_numbers) if page_numbers else 1
        print(f"✅ 총 페이지 수: {total_pages}")
        return total_pages
    
    def get_ingredients(self):
        """모든 성분 데이터를 크롤링하여 리스트 반환 (중복 mol_id 제외 처리)"""
        ingredients = []
        collected_mol_ids = set()  # ✅ 수집된 mol_id 추적

        # ✅ URL 로드 (1페이지)
        self.driver.get(self.herb_url)
        time.sleep(2)

        total_pages = self.get_total_pages()
        print(f"📄 총 {total_pages} 페이지 예상 - 성분 크롤링 시작...")

        for page in range(1, total_pages + 1):
            try:
                print(f"➡️ {self.herb_name} - 페이지 {page} 크롤링 중...")

                # ✅ 첫 페이지 제외 시 클릭
                if page > 1:
                    pagination_links = self.driver.find_elements(By.CSS_SELECTOR, ".k-pager-numbers .k-link")
                    page_link = next(
                        (link for link in pagination_links
                        if link.get_attribute("data-page") == str(page)
                        and link.get_attribute("data-page").isdigit()), None)

                    if page_link:
                        self.driver.execute_script("arguments[0].click();", page_link)
                        WebDriverWait(self.driver, 10).until(EC.staleness_of(page_link))
                        time.sleep(2)

                soup = BeautifulSoup(self.driver.page_source, "html.parser")
                table = soup.select_one("#grid table tbody")

                if not table:
                    print(f"⚠️ 페이지 {page}에 테이블 없음. 크롤링 중단.")
                    break

                rows = table.find_all("tr")
                new_ingredients = []

                for row in rows:
                    cols = row.find_all("td")
                    if len(cols) < 10:
                        continue

                    mol_id = cols[0].text.strip()

                    # ✅ 이미 수집된 mol_id는 건너뜀
                    if mol_id in collected_mol_ids:
                        print(f"🔁 중복 mol_id 발견: {mol_id} → 해당 성분 건너뜀")
                        continue

                    mol_name_tag = cols[1].find("a")
                    mol_name = mol_name_tag.text.strip() if mol_name_tag else ""
                    mol_url = self.MOLECULE_URL.format(path=mol_name_tag["href"]) if mol_name_tag else ""
                    mw = cols[2].text.strip()
                    alogp = cols[3].text.strip()
                    hdon = cols[4].text.strip()
                    hacc = cols[5].text.strip()
                    ob = float(cols[6].text.strip()) if cols[6].text.strip() else 0
                    caco2 = cols[7].text.strip()
                    bbb = cols[8].text.strip()
                    dl = float(cols[9].text.strip()) if cols[9].text.strip() else 0
                    fasa = cols[10].text.strip()
                    halflife = cols[11].text.strip()

                    ingredient = {
                        "mol_id": mol_id,
                        "mol_name": mol_name,
                        "mol_url": mol_url,
                        "mw": mw,
                        "alogp": alogp,
                        "hdon": hdon,
                        "hacc": hacc,
                        "ob": ob,
                        "caco2": caco2,
                        "bbb": bbb,
                        "dl": dl,
                        "fasa": fasa,
                        "halflife": halflife
                    }

                    new_ingredients.append(ingredient)
                    collected_mol_ids.add(mol_id)  # ✅ mol_id 등록

                ingredients.extend(new_ingredients)

                # ✅ 이번 페이지에서 새 성분을 수집하지 못했으면 중단
                if not new_ingredients:
                    print(f"⚠️ 페이지 {page}에서 새로운 성분 없음 → 크롤링 중단")
                    break

            except Exception as e:
                print(f"❌ 페이지 {page} 크롤링 중 오류 발생: {e}")
                continue

        print(f"✅ {self.herb_name} 성분 크롤링 완료. 총 {len(ingredients)}개 성분 수집됨.")
        return ingredients
    
    def get_targets(self, ingredients, max_retries=5):
        """성분별 타겟 크롤링 (로딩 안정성 개선 및 StaleElementReference 해결)"""
        targets = []

        for idx, ingredient in enumerate(ingredients, 1):
            mol_url = ingredient.get("mol_url")
            if not mol_url:
                print(f"⚠️ {ingredient['mol_name']}에 mol_url 없음 - 건너뜀")
                continue

            print(f"🔎 [{idx}/{len(ingredients)}] {ingredient['mol_name']} 타겟 크롤링 중...")

            retries = 0
            while retries < max_retries:
                try:
                    # ✅ 페이지 로드 및 로딩 대기
                    self.driver.get(mol_url)
                    WebDriverWait(self.driver, 15).until(
                        EC.presence_of_element_located((By.TAG_NAME, "body"))
                    )
                    time.sleep(1)  # 잠깐의 대기

                    # ✅ 초기 페이지 수 확인
                    pagination_links = self.driver.find_elements(By.CSS_SELECTOR, "#kendo_target .k-pager-numbers .k-link")
                    total_pages = max(
                        [int(link.get_attribute("data-page")) for link in pagination_links if link.get_attribute("data-page")],
                        default=1
                    )

                    page = 1
                    visited_pages = set()

                    while True:
                        print(f"📂 타겟 페이지 {page}/{total_pages}")

                        # ✅ 테이블 로딩 대기 (최대 10초)
                        try:
                            WebDriverWait(self.driver, 10).until(
                                EC.presence_of_element_located((By.CSS_SELECTOR, "#kendo_target table tbody"))
                            )
                        except TimeoutException:
                            print("⚠️ 테이블 로딩 실패 - N/A 값으로 대체")
                            targets.append({
                                "mol_id": ingredient["mol_id"],
                                "mol_name": ingredient["mol_name"],
                                "target_name": "N/A",
                                "target_id": "N/A",
                                "drugbank_id": "N/A",
                                **{key: ingredient[key] for key in ["mw", "alogp", "hdon", "hacc", "ob", "caco2", "bbb", "dl", "fasa", "halflife"]}
                            })
                            break

                        # ✅ 타겟 정보 수집
                        soup = BeautifulSoup(self.driver.page_source, "html.parser")
                        table = soup.select_one("#kendo_target table tbody")

                        if table:
                            for row in table.find_all("tr"):
                                cols = row.find_all("td")
                                if len(cols) < 2:
                                    continue

                                targets.append({
                                    "mol_id": ingredient["mol_id"],
                                    "mol_name": ingredient["mol_name"],
                                    "target_name": cols[0].text.strip() or "N/A",
                                    "target_id": cols[0].find("a")["href"].split("=")[-1] if cols[0].find("a") else "N/A",
                                    "drugbank_id": cols[1].find("a")["href"].split("/")[-1] if cols[1].find("a") else "N/A",
                                    **{key: ingredient[key] for key in ["mw", "alogp", "hdon", "hacc", "ob", "caco2", "bbb", "dl", "fasa", "halflife"]}
                                })

                        visited_pages.add(page)

                        # ✅ 마지막 페이지 도달 시 종료
                        if page >= total_pages:
                            print("✅ 마지막 페이지 도달 - 타겟 크롤링 종료")
                            break

                        # ✅ 11페이지 도달 시 페이지 수 재확인
                        if page == 11:
                            pagination_links = self.driver.find_elements(By.CSS_SELECTOR, "#kendo_target .k-pager-numbers .k-link")
                            updated_total_pages = max(
                                [int(link.get_attribute("data-page")) for link in pagination_links if link.get_attribute("data-page")],
                                default=total_pages
                            )
                            if updated_total_pages > total_pages:
                                print(f"🔄 페이지 수 재확인: {total_pages} → {updated_total_pages}")
                                total_pages = updated_total_pages

                        # ✅ 다음 페이지 클릭
                        pagination_links = self.driver.find_elements(By.CSS_SELECTOR, "#kendo_target .k-pager-numbers .k-link")
                        next_page_link = next(
                            (link for link in pagination_links if int(link.get_attribute("data-page")) == page + 1),
                            None
                        )

                        if not next_page_link:
                            print("✅ 더 이상 페이지 없음 - 타겟 크롤링 종료")
                            break

                        # ✅ 클릭 시 새 요소로 대체 및 대기
                        self.driver.execute_script("arguments[0].click();", next_page_link)
                        WebDriverWait(self.driver, 10).until(
                            EC.staleness_of(next_page_link)
                        )
                        page += 1
                        time.sleep(1)  # 클릭 후 잠시 대기

                    break  # ✅ 크롤링 성공 시 재시도 중단

                except Exception as e:
                    retries += 1
                    print(f"⚠️ {mol_url} 크롤링 실패 (시도 {retries}/{max_retries}): {e}")
                    if retries == max_retries:
                        print(f"❌ {mol_url} 최대 재시도 실패 - 건너뜀")

        print(f"✅ 타겟 크롤링 완료. 총 {len(targets)}개 타겟 수집됨.")
        return targets


    def scrape(self):
        """전체 크롤링 (성분 + 타겟)"""
        print(f"🚀 {self.herb_name} 크롤링 시작...")
        ingredients = self.get_ingredients()
        targets = self.get_targets(ingredients)
        return {"herb": self.herb_name, "ingredients": ingredients, "targets": targets}
