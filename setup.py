# setup.py

from setuptools import setup, find_packages

def load_requirements(filename="requirements.txt"):
    """📦 requirements.txt 파일에서 의존성 불러오기"""
    with open(filename, encoding="utf-8") as f:
        return f.read().splitlines()


setup(
    name="herb-scraper",  # 📦 프로젝트 이름
    version="1.0.0",  # 🔖 버전
    description="🌿 A pipeline for scraping and processing herb-related data.",  # 📝 설명
    author="Kim Hyeonseo",  # 🧑‍💻 작성자
    author_email="neulbokim@sogang.ac.kr",  # 📧 이메일
    url="https://github.com/neulbokim/herb-scraper",  # 🌍 프로젝트 URL
    packages=find_packages(exclude=["tests*", "backup*", "docs*"]),  # 📂 모든 모듈 포함 (테스트 및 백업 제외)
    install_requires=load_requirements(),  # 📦 필수 의존성 불러오기
    python_requires=">=3.8",  # 🐍 Python 최소 버전
    extras_require={  # 🧩 선택적 의존성
        "dev": ["pytest", "black", "flake8"],  # 개발 및 코드 스타일링 도구
        "docs": ["sphinx"],  # 문서화 도구
    },
    entry_points={  # 🖥️ CLI 명령어 등록
        "console_scripts": [
            "herb-scraper=scripts.main:main",  # `herb-scraper` 명령어로 실행
        ],
    },
    classifiers=[  # 🏷️ PyPI 분류
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    include_package_data=True,  # 📦 패키지에 추가 파일 포함
    zip_safe=False,  # 🚫 압축 설치 비활성화 (일부 파일 액세스 문제 방지)
)
