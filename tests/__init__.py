# tests/__init__.py

"""
✅ 테스트 모듈 초기화 파일

- pytest에서 `tests/` 디렉토리를 패키지로 인식하도록 설정
- 경로 문제 해결 (모듈 임포트 시 상대경로 문제 방지)
- 테스트 환경 설정 및 공통 초기화 작업 포함
"""

import sys
import os

# ✅ 프로젝트 루트 디렉토리를 sys.path에 추가 (경로 문제 방지)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

# ✅ 환경 변수 설정 (테스트용 설정 적용 필요 시)
os.environ["TESTING"] = "True"

# ✅ 공통 로그 출력
print(f"✅ 테스트 환경 초기화 완료 (BASE_DIR: {BASE_DIR})")
