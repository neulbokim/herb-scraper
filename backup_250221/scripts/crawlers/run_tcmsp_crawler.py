# scripts/crawlers/run_tcmsp_crawler.py

from modules.crawlers.tcmsp_crawler import crawl_tcmsp
from modules.constants import HERB_LIST  # 변경된 부분: HERB_LIST에서 약재명 리스트 가져오기
from modules.utils import setup_logger

logger = setup_logger("run_tcmsp_crawler")

def main():
    logger.info("🚀 [TCMSP 크롤링] 시작")

    for herb in HERB_LIST:
        logger.info(f"🌿 {herb} 크롤링 중...")
        crawl_tcmsp(herb)

    logger.info("✅ [TCMSP 크롤링] 전체 완료")

if __name__ == "__main__":
    main()
