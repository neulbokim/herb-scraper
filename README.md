# 🌿 HERB Scraper 프로젝트

---

## 📌 **프로젝트 개요**  
herb-scraper는 TCMSP (Traditional Chinese Medicine Systems Pharmacology) 데이터베이스에서 한약재 데이터를 자동으로 크롤링하고 전처리할 수 있는 Python 기반의 스크래퍼입니다. 연구자 및 개발자가 빠르게 데이터를 수집하고 필터링하여 네트워크 약리학 연구에 활용할 수 있도록 지원합니다.

---

## ✅ **주요 기능:**  
1. **TCMSP 데이터 크롤링**: 지정된 한약재의 성분 및 타겟 정보를 수집합니다.
2. **데이터 전처리(필터링)**: OB(경구이용률)와 DL(약물 유사성) 기준으로 성분과 타겟 데이터를 필터링합니다.
3. **다양한 포맷 지원**: 크롤링 및 필터링된 데이터를 JSON, CSV, Excel 파일로 저장합니다.
4. **사용자 친화적 설정**: config/settings.py에서 데이터 경로 및 필터링 임계값을 손쉽게 변경할 수 있습니다.

---

## 🗂️ **디렉토리 구조**
```bash
herb-scraper/
├── README.md                          # ✅ 프로젝트 설명 문서
├── requirements.txt                   # ✅ Python 패키지 목록
├── venv/                              # ✅ 가상환경 디렉토리
│
├── config/                            # ⚙️ 설정 관련
│   └── settings.py                    # 환경 설정 (경로, 필터링 임계값 등)
│
├── modules/                           # 🧩 코드 모듈 (TCMSP 전용)
│   ├── data_utils.py                  # 🌐 데이터 저장/불러오기
│   ├── logger.py                      # 📝 로그 기록
│   └── tcmsp_utils.py                 # 🌍 TCMSP 크롤링 모듈
│
├── preprocess/                        # 🧹 전처리 관련
│   └── tcmsp_process.py               # 데이터 필터링
│
├── scripts/                           # 🚀 실행 스크립트
│   └── tcmsp_scraper.py               # TCMSP 크롤링 실행 스크립트
│
└── data/                              # 📂 데이터 저장
    └── tcmsp/                         # 📥 TCMSP 데이터
```

---
## 🗺️ **📊 파이프라인 흐름도**

```mermaid
graph TD
    A[herb-scraper/] --> B[README.md: 프로젝트 설명 문서]
    A --> C[requirements.txt: Python 패키지 목록]
    A --> D[venv/: 가상환경 디렉토리]

    A --> E[config/: 설정 관련]
    E --> E1[settings.py: 경로 및 필터링 임계값 설정]

    A --> F[modules/: 코드 모듈 (TCMSP 전용)]
    F --> F1[data_utils.py: 데이터 저장/불러오기 및 WebDriver 설정]
    F --> F2[logger.py: 로그 기록 모듈]
    F --> F3[tcmsp_utils.py: TCMSP 크롤링 모듈]

    A --> G[preprocess/: 전처리 관련]
    G --> G1[tcmsp_process.py: 데이터 필터링 및 저장]

    A --> H[scripts/: 실행 스크립트]
    H --> H1[tcmsp_scraper.py: TCMSP 크롤링 실행 스크립트]

    A --> I[data/: 데이터 저장]
    I --> I1[tcmsp/: TCMSP 원본 및 필터링 데이터]
```

---

## 🛠️ **설치 및 실행 방법**
### 1️⃣ 가상환경 설정
```bash
python -m venv venv
source venv/bin/activate      # Mac/Linux
venv\Scripts\activate        # Windows
pip install -r requirements.txt
```

### 2️⃣ 크롤링 실행
```bash
python scripts/tcmsp_scraper.py
```
- **크롤링 대상 약재**: scripts/tcmsp_scraper.py 내부의 herbs 딕셔너리에서 수정할 수 있습니다.
- **데이터 저장 경로**: 크롤링된 데이터는 data/tcmsp/에 JSON 및 CSV 형식으로 저장됩니다.

### 3️⃣ 크롤링 실행
```bash
python preprocess/tcmsp_process.py
```
- **필터링 기준**: config/settings.py에서 OB_THRESHOLD와 DL_THRESHOLD 값 조정 가능합니다.
- **출력 결과**: 필터링된 데이터는 data/tcmsp/ 폴더에 JSON, CSV, Excel 파일로 저장됩니다.


---
## ⚙️ 설정 설명 (`config/settings.py`)

```markdown
| 설정 변수              | 설명                             | 기본값    |
|-----------------------|----------------------------------|---------|
| `OB_THRESHOLD`        | OB(경구이용률) 필터링 임계값     | `30`    |
| `DL_THRESHOLD`        | DL(약물 유사성) 필터링 임계값    | `0.18`  |
| `HERB_GROUP_NAME`     | 데이터 그룹 이름                | `전체_약재` |
| `RAW_DATA_PATH`       | 크롤링 원본 데이터 경로         | 자동 설정 |
| `PROCESSED_EXCEL_PATH`| 필터링 데이터 Excel 저장 경로   | 자동 설정 |
```

---

## 📊 출력 데이터 예시

### ✅ 크롤링된 원본 데이터 (`tcmsp_raw_results_전체_약재.json`)

```json
{
  "황금": {
    "ingredients": [
      {
        "mol_id": "MOL000173",
        "mol_name": "baicalin",
        "ob": 41.15,
        "dl": 0.75,
        "mol_url": "https://tcmsp-e.com/..."
      }
    ],
    "targets": [
      {
        "mol_id": "MOL000173",
        "target_name": "EGFR",
        "drugbank_id": "DB00001"
      }
    ]
  }
}
```

---

### ✅ 필터링된 데이터 (`tcmsp_filtered_targets_전체_약재.xlsx`)

```markdown
| mol_id     | mol_name | ob    | dl    | target_name | drugbank_id |
|------------|----------|-------|-------|-------------|-------------|
| MOL000173  | baicalin | 41.15 | 0.75  | EGFR        | DB00001     |
```

---

## 🧩 주요 코드 설명

```markdown
### 📁 `modules/`
- **`data_utils.py`**: 데이터 저장/불러오기 및 Selenium WebDriver 설정.
- **`logger.py`**: 일관된 로그 출력 지원.
- **`tcmsp_utils.py`**: 성분 및 타겟 크롤링 로직 포함.

### 📁 `preprocess/`
- **`tcmsp_process.py`**: 크롤링된 데이터를 OB, DL 기준으로 필터링 및 파일 저장.

### 📁 `scripts/`
- **`tcmsp_scraper.py`**: 크롤링을 시작하는 메인 실행 스크립트.
```

---


## 📜 **라이선스**
MIT License  
© 2025 상지한의 학술제

---

## 👩‍💻 **개발자 정보**
프로젝트 담당: 서강대학교 국어국문학과 김현서  
📧 이메일: neulbokim@sogang.ac.kr  
🌍 GitHub: github.com/neulbokim