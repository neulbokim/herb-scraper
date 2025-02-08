import time
import requests
import json

BATMAN_TCM_URL = "http://batman2api.cloudna.cn/queryTarget"

def get_target_proteins(pubchem_list):
    """BATMAN-TCM API를 이용해 여러 PubChem ID의 표적 단백질을 조회"""
    results = {}

    # ✅ API에 맞는 요청 데이터 형식으로 변환
    payload = {
        "content": [
            {
                "clusterName": "PubChem_Target_Search",
                "type": "compound",  
                "list": pubchem_list  
            }
        ],
        "pvalue": 0.05,
        "userInScore": 30
    }

    try:
        print(f"🔍 PubChem ID {len(pubchem_list)}개에 대한 표적 단백질 조회 중...")
        response = requests.post(BATMAN_TCM_URL, json=payload)

        if response.status_code == 200:
            data = response.json()

            # ✅ API 응답이 리스트인 경우 처리
            if isinstance(data, list):
                for compound in data:
                    pubchem_id = compound.get("cid", "")
                    targets = compound.get("target", [])  # 표적 단백질 정보 가져오기
                    results[pubchem_id] = targets

                    print(f"✅ {pubchem_id}: {len(targets)}개 타겟 단백질 수집 완료")

            else:
                print(f"❌ 예상과 다른 응답 형식: {type(data)}")
                print(json.dumps(data, indent=4, ensure_ascii=False))

        else:
            print(f"❌ 요청 실패: {response.status_code}")

    except Exception as e:
        print(f"❌ 오류 발생: {e}")

    time.sleep(1)  # ✅ BATMAN-TCM 서버 부하 방지를 위한 1초 대기

    return results
