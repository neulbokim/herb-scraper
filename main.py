from crawler.oasis_scraper import OasisScraper
from crawler.pubchem_scraper import PubChemScraper
from crawler.swissadme_scraper import SwissAdmeScraper
from crawler.utils import save_json, delay_request

if __name__ == "__main__":
    oasis_scraper = OasisScraper()
    pubchem_scraper = PubChemScraper()
    swissadme_scraper = SwissAdmeScraper()

    # 1. 오아시스 크롤링 (약재 목록 + 상세보기 링크 수집)
    herb_links = oasis_scraper.scrape_oasis()

    # 2. 전체 성분에 대한 PubChem 및 SwissADME 정보 크롤링
    results = {}

    for herb, url in herb_links.items():
        print(f"\n[INFO] Processing {herb}...")

        # 오아시스 상세 페이지에서 성분과 PubChem ID 추출
        pubchem_data = pubchem_scraper.extract_pubchem_id_from_oasis(herb)

        if not pubchem_data:
            print(f"[WARNING] {herb}의 PubChem 데이터를 찾을 수 없음.")
            continue

        # JSON 저장 구조화
        results[herb] = {
            "Total Components": len(pubchem_data),
            "Components": {}
        }

        for name, pubchem_id in pubchem_data.items():
            print(f"[INFO] Found PubChem ID for {herb} - {name}: {pubchem_id}")

            # PubChem에서 SMILES 가져오기
            smiles = pubchem_scraper.fetch_smiles(pubchem_id)

            if not smiles:
                print(f"[WARNING] {herb} - {name}의 SMILES 정보를 찾을 수 없음.")
                continue

            print(f"[INFO] Found SMILES for {herb} - {name}: {smiles}")

            # SwissADME에서 분자 정보 가져오기
            molecule_info = swissadme_scraper.fetch_molecule_data(smiles)

            if not molecule_info:
                print(f"[WARNING] {herb} - {name}의 SwissADME 정보를 찾을 수 없음.")
                continue

            print(f"[INFO] Retrieved molecular data for {herb} - {name}")

            # 데이터 저장 (약재 → 성분별로 정보 저장)
            results[herb]["Components"][name] = {
                "PubChem ID": pubchem_id,
                "SMILES": smiles,
                "Molecular Data": molecule_info
            }

            # 딜레이 추가 (서버 부하 방지)
            delay_request(2)

    # 3. JSON 저장 (구조화된 데이터)
    save_json(results, "herb_components_results.json", folder="data/processed")

    print("\n[INFO] 모든 데이터를 성공적으로 저장했습니다.")
