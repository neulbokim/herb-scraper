# 🌿 HERB Scraper 프로젝트

---

## 📌 **프로젝트 개요**  
**herb-scraper**는 HERB 데이터베이스와 TCMSP (Traditional Chinese Medicine Systems Pharmacology) 데이터베이스에서 한약재 데이터를 자동으로 크롤링하고 전처리할 수 있는 Python 기반의 스크래퍼입니다.  

✅ **데이터 수집 흐름:**  
- **지황:** HERB 데이터베이스를 통해 `herb_scraper.py` → `ingredient_scraper.py`로 크롤링합니다.  
- **기타 약재:** TCMSP 데이터베이스를 통해 `tcmsp_scraper.py`로 크롤링합니다.  

이 프로젝트는 연구자 및 개발자가 빠르게 데이터를 수집하고 필터링하여 네트워크 약리학 연구에 활용할 수 있도록 지원합니다.

---

## ✅ **주요 기능:**  
1. **HERB & TCMSP 데이터 크롤링**: 지황 및 기타 한약재의 성분과 타겟 정보를 수집합니다.  
2. **데이터 전처리(필터링)**: OB(경구이용률)와 DL(약물 유사성) 기준으로 성분과 타겟 데이터를 필터링합니다.  
3. **다양한 포맷 지원**: 크롤링 및 필터링된 데이터를 JSON, CSV, Excel 파일로 저장합니다.  
4. **사용자 친화적 설정**: `config/settings.py`에서 데이터 경로 및 필터링 임계값을 손쉽게 변경할 수 있습니다.  

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
├── modules/                           # 🧩 코드 모듈
│   ├── data_utils.py                  # 🌐 데이터 저장/불러오기 및 WebDriver 설정
│   ├── logger.py                      # 📝 로그 기록 모듈
│   ├── herb_utils.py                  # 🌱 HERB 데이터 크롤링 모듈
│   └── tcmsp_utils.py                 # 🌍 TCMSP 데이터 크롤링 모듈
│
├── preprocess/                        # 🧹 전처리 관련
│   └── tcmsp_process.py               # TCMSP 데이터 필터링
│
├── scripts/                           # 🚀 실행 스크립트
│   ├── herb_scraper.py                # 🌿 지황 성분 URL 크롤링 스크립트 (HERB 전용)
│   ├── ingredient_scraper.py         # 🧪 지황 성분 상세 정보 크롤링 스크립트
│   └── tcmsp_scraper.py               # 🪴 기타 한약재 TCMSP 크롤링 스크립트
│
└── data/                              # 📂 데이터 저장
    └── herb/                          # 📥 지황 데이터 (HERB 원본 및 상세 정보)
    └── tcmsp/                         # 📥 기타 약재 TCMSP 데이터
```

---
## 🗺️ **📊 파이프라인 흐름도**
```mermaid
graph TD
    subgraph 지황 (HERB 데이터)
        A[herb_scraper.py: 지황 성분 URL 수집] --> B[herb_ingredient_urls_지황.json 저장]
        B --> C[ingredient_scraper.py: 지황 성분 상세 크롤링]
        C --> D[JSON, CSV, XLSX로 저장 (data/herb/)]
    end

    subgraph 기타 약재 (TCMSP 데이터)
        E[tcmsp_scraper.py: 기타 한약재 성분 및 타겟 크롤링] --> F[JSON, CSV 저장 (data/tcmsp/)]
    end

    subgraph 전처리 및 분석
        D --> G[tcmsp_process.py: 데이터 필터링]
        F --> G
        G --> H[필터링된 Excel 데이터 생성 (data/tcmsp/)]
    end
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

### 2️⃣ 크롤링 및 데이터 수집

#### 🌿 **지황 (HERB 데이터)**
##### 📝 (1단계) 성분 URL 크롤링
```bash
python scripts/herb_scraper.py
```
- **설명**: HERB 데이터베이스에서 지황의 성분 URL을 수집합니다.
- **출력 파일**: `data/herb/herb_ingredient_urls_지황.json`

##### 🧪 (2단계) 성분 상세 정보 크롤링
```bash
python scripts/ingredient_scraper.py
```
- **설명**: 수집한 URL을 기반으로 각 성분의 상세 정보를 크롤링합니다.
- **출력 파일**: `data/herb/herb_ingredients_지황.json`, `.csv`, `.xlsx`

---

#### 🪴 **기타 청열약(황금, 황련, 황백, 고삼, 지모, 지황, 치자) (TCMSP 데이터)**
##### 🌍 성분 및 타겟 크롤링
```bash
python scripts/tcmsp_scraper.py
```
- **설명**: TCMSP 데이터베이스에서 지황을 제외한 청열약의 성분 및 타겟 정보를 크롤링합니다.
- **출력 파일**: `data/tcmsp/` 폴더 내 JSON 및 CSV 파일

---

### 3️⃣ 데이터 전처리 및 필터링
```bash
python preprocess/tcmsp_process.py
```
- **설명**: HERB와 TCMSP에서 수집된 데이터를 OB 및 DL 기준으로 필터링합니다.
- **출력 파일**: `data/tcmsp/tcmsp_filtered_targets_전체_약재.xlsx`
- **임계값 조정**: `config/settings.py`의 `OB_THRESHOLD` 및 `DL_THRESHOLD` 변경 가능

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

## 📊 **출력 데이터 예시**

### ✅ **지황 (HERB) 데이터 예시**
#### 1️⃣ **성분 URL 크롤링 결과** (`herb_ingredient_urls_지황.json`)
```json
{
  "지황": [
    "http://herb.ac.cn/Detail/?v=HBIN000001",
    "http://herb.ac.cn/Detail/?v=HBIN000002"
  ]
}
```

#### 2️⃣ **성분 상세 정보 크롤링 결과** (`herb_ingredients_지황.json`)
```json
{
  "http://herb.ac.cn/Detail/?v=HBIN000001": {
    "ingredient_name": "catalpol",
    "molecule_smile": "C1COC2C(C1)C(O)C(O)C(O)C2O",
    "PubChem ID": "CID12345",
    "CAS ID": "2415-24-9"
  }
}
```

---

### ✅ **기타 약재 (TCMSP) 데이터 예시**
#### 1️⃣ **성분 및 타겟 크롤링 결과** (`tcmsp_raw_results_전체_약재.json`)
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

#### 2️⃣ **필터링된 데이터** (`tcmsp_filtered_targets_전체_약재.xlsx`)
```markdown
| mol_id     | mol_name | ob    | dl    | target_name | drugbank_id |
|------------|----------|-------|-------|-------------|-------------|
| MOL000173  | baicalin | 41.15 | 0.75  | EGFR        | DB00001     |
```

---

## 🧩 **주요 코드 설명**
```markdown
### 📁 `modules/`
- **`data_utils.py`**: 데이터 저장/불러오기 및 WebDriver 설정.
- **`logger.py`**: 로그 기록 모듈.
- **`herb_utils.py`**: HERB 데이터 크롤링 모듈 (지황 전용).
- **`tcmsp_utils.py`**: TCMSP 데이터 크롤링 모듈 (기타 약재 전용).

### 📁 `scripts/`
- **`herb_scraper.py`**: 지황 성분 URL 크롤링.
- **`ingredient_scraper.py`**: 지황 성분 상세 크롤링 및 데이터 저장.
- **`tcmsp_scraper.py`**: 기타 한약재 크롤링.

### 📁 `preprocess/`
- **`tcmsp_process.py`**: 데이터 전처리 및 필터링.
```

---

## 📜 **라이선스**  
MIT License  
© 2025 상지한의 학술제  

---

## 👩‍💻 **개발자 정보**
- **프로젝트 담당**: 서강대학교 국어국문학과 김현서  
- **📧 이메일**: neulbokim@sogang.ac.kr  
- **🌍 GitHub**: [github.com/neulbokim](https://github.com/neulbokim)  

---