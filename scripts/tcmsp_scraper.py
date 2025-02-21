# scripts/tcmsp_scraper.py
from config.settings import HERB_GROUP_NAME, TCMSP_DIR
from modules.tcmsp_utils import TCMSPScraper
from modules.data_utils import save_to_json, save_to_csv

if __name__ == "__main__":
    herbs = {
        "황금": "https://tcmsp-e.com/tcmspsearch.php?qr=Scutellariae%20Radix&qsr=herb_en_name&token=594e7113175c945ed8fafb065b29ac0c",
        "황련": "https://tcmsp-e.com/tcmspsearch.php?qr=Coptidis%20Rhizoma&qsr=herb_en_name&token=594e7113175c945ed8fafb065b29ac0c",
        "치자": "https://tcmsp-e.com/tcmspsearch.php?qr=Gardeniae%20Fructus&qsr=herb_en_name&token=594e7113175c945ed8fafb065b29ac0c",
        "황백": "https://tcmsp-e.com/tcmspsearch.php?qr=Phellodendri%20Chinrnsis%20Cortex&qsr=herb_en_name&token=594e7113175c945ed8fafb065b29ac0c",
        "고삼": "https://tcmsp-e.com/tcmspsearch.php?qr=Sophorae%20Flavescentis%20Radix&qsr=herb_en_name&token=594e7113175c945ed8fafb065b29ac0c",
        "지모": "https://tcmsp-e.com/tcmspsearch.php?qr=Anemarrhenae%20Rhizoma&qsr=herb_en_name&token=594e7113175c945ed8fafb065b29ac0c"
    }

    results = {}

    for herb, url in herbs.items():
        print(f"🚀 {herb} 크롤링 시작...")
        scraper = TCMSPScraper(herb, url)
        result = scraper.scrape()

        results[herb] = result

        save_to_json(result["ingredients"], f"tcmsp_{herb}_raw_ingredients.json", "tcmsp")
        save_to_csv(result["ingredients"], f"tcmsp_{herb}_raw_ingredients.csv", "tcmsp")
        save_to_json(result["targets"], f"tcmsp_{herb}_raw_targets.json", "tcmsp")
        save_to_csv(result["targets"], f"tcmsp_{herb}_raw_targets.csv", "tcmsp")
        print(f"✅ {herb} raw 데이터 저장 완료!")

    save_to_json(results, f"tcmsp_raw_results_{HERB_GROUP_NAME}.json", "tcmsp")
    print("🚀 전체 크롤링 및 raw 데이터 저장 완료!")
