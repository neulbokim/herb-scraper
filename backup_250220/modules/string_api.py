import requests
import time
from modules.data_utils import save_to_json

# ✅ STRING API 기본 설정
STRING_API_URL = "https://string-db.org/api"
SPECIES_ID = 9606  # 인간 (Homo sapiens)
CALLER_IDENTITY = "ppi_fetcher_script"
CALLER_IDENTITY_TARGET = "compound_target_fetcher"


def get_string_ids(identifiers):
    """STRING API를 사용하여 Gene Name 또는 UniProt ID를 STRING ID로 변환"""
    url = f"{STRING_API_URL}/json/get_string_ids"
    params = {
        "identifiers": "%0d".join(identifiers),
        "species": SPECIES_ID,
        "caller_identity": CALLER_IDENTITY
    }

    response = requests.post(url, data=params)
    time.sleep(1)  # 서버 부하 방지를 위해 1초 대기

    if response.status_code == 200:
        return response.json()  # ✅ 응답을 JSON 형태로 그대로 반환
    else:
        print(f"⚠️ STRING API 요청 실패! 상태 코드: {response.status_code}")
        return []


def get_ppi_data(string_ids, limit=10, batch_size=1000):
    """STRING API를 사용하여 PPI (단백질 상호작용) 데이터를 가져옴"""
    url = f"{STRING_API_URL}/tsv/interaction_partners"

    ppi_results = []

    # 🔹 ID를 batch_size 크기로 나눠서 요청
    for i in range(0, len(string_ids), batch_size):
        batch = string_ids[i:i + batch_size]
        params = {
            "identifiers": "%0d".join(batch),  # ✅ batch 단위로 ID를 문자열로 변환
            "species": SPECIES_ID,
            "limit": limit,
            "caller_identity": CALLER_IDENTITY
        }

        print(f"🔹 PPI API 요청 (batch {i//batch_size+1}/{len(string_ids)//batch_size+1}): {len(batch)}개 ID")

        response = requests.post(url, data=params)
        time.sleep(1)  # ✅ API 부하 방지

        if response.status_code != 200:
            print(f"⚠️ PPI API 요청 실패! 상태 코드: {response.status_code}")
            continue

        lines = response.text.strip().split("\n")

        # ✅ 첫 번째 행(헤더) 제거
        if len(lines) > 1:
            lines = lines[1:]

        print(f"🔹 PPI API 응답 (batch {i//batch_size+1}):\n{response.text[:500]}")  # ✅ 응답 미리보기

        for line in lines:
            parts = line.split("\t")
            if len(parts) >= 6:
                ppi_results.append({
                    "STRING ID A": parts[0],
                    "STRING ID B": parts[1],
                    "Protein A": parts[2],
                    "Protein B": parts[3],
                    "NCBI Taxon ID": parts[4],
                    "Combined Score": parts[5]
                })

    print(f"✅ PPI 데이터 개수: {len(ppi_results)}")
    return ppi_results



def get_compound_targets(compounds):
    """STRING API를 사용하여 특정 화합물(성분)의 타겟 단백질을 가져옴"""
    url = f"{STRING_API_URL}/tsv/chemical_interactions"
    all_results = []

    for compound in compounds:
        compound_name = compound.get("ingredient_name")
        pubchem_id = compound.get("PubChem id", "").strip()

        # 🔹 PubChem ID 우선, 없으면 화합물 이름 사용
        query_identifier = pubchem_id if pubchem_id else compound_name

        if not query_identifier:
            print(f"⚠️ {compound_name}는 유효한 식별자가 없습니다. 스킵합니다.")
            continue

        params = {
            "identifiers": query_identifier,
            "species": SPECIES_ID,
            "caller_identity": CALLER_IDENTITY_TARGET
        }

        print(f"🔹 STRING API 요청 (화합물: {query_identifier})")
        response = requests.post(url, data=params)
        time.sleep(1)  # ✅ API 부하 방지

        if response.status_code != 200:
            print(f"⚠️ STRING API 요청 실패! 상태 코드: {response.status_code} ({query_identifier})")
            continue

        lines = response.text.strip().split("\n")

        # ✅ 첫 번째 행(헤더) 제거
        if len(lines) > 1:
            lines = lines[1:]

        for line in lines:
            parts = line.split("\t")
            if len(parts) >= 6:
                all_results.append({
                    "Compound": query_identifier,
                    "STRING ID": parts[0],
                    "Protein": parts[2],
                    "NCBI Taxon ID": parts[3],
                    "Combined Score": parts[4]
                })

    print(f"✅ 총 {len(all_results)}개의 타겟 단백질 데이터 수집 완료!")
    return all_results