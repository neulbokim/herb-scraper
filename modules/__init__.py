import logging

# 로깅 설정
logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

logging.info("✅ modules 패키지가 로드되었습니다.")

# 패키지화 설정
__all__ = ["batman_tcm_utils", "data_utils", "herb_utils", "preprocessing", "swissadme_utils"]

# 각 모듈 자동 import
from .batman_tcm_utils import *
from .data_utils import *
from .herb_utils import *
from .preprocessing import *
from .swissadme_utils import *