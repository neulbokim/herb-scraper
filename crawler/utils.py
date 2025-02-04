import requests
import os
import json
import time
from config import HEADERS

def fetch_html(url):
    """
    URL에 요청을 보내 HTML을 가져오는 함수.
    예외 처리를 포함하여 요청이 실패하면 None을 반환.
    """
    try:
        response = requests.get(url, headers=HEADERS)
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"[ERROR] {url} 요청 실패: {e}")
        return None


def save_html(html, filename, folder="data/raw"):
    """
    HTML을 파일로 저장하는 함수.
    """
    os.makedirs(folder, exist_ok=True)
    file_path = os.path.join(folder, filename)
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"[INFO] HTML 저장 완료: {file_path}")


def load_html(filename, folder="data/raw"):
    """
    저장된 HTML 파일을 불러오는 함수.
    """
    file_path = os.path.join(folder, filename)
    if not os.path.exists(file_path):
        print(f"[WARNING] 파일 없음: {file_path}")
        return None
    
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()

def post_html(url, data):
    """
    특정 URL에 POST 요청을 보내고 HTML을 반환하는 함수.
    요청이 실패하면 None 반환.
    """
    try:
        response = requests.post(url, data=data, headers=HEADERS)
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"[ERROR] {url} POST 요청 실패: {e}")
        return None

def save_json(data, filename, folder="data/processed"):
    """
    JSON 데이터를 파일로 저장하는 함수.
    """
    os.makedirs(folder, exist_ok=True)
    file_path = os.path.join(folder, filename)
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    print(f"[INFO] JSON 저장 완료: {file_path}")


def load_json(filename, folder="data/processed"):
    """
    저장된 JSON 데이터를 불러오는 함수.
    """
    file_path = os.path.join(folder, filename)
    if not os.path.exists(file_path):
        print(f"[WARNING] 파일 없음: {file_path}")
        return None
    
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)


def delay_request(seconds=2):
    """
    서버 부하 방지를 위해 요청 사이에 일정 시간 대기하는 함수.
    """
    print(f"[INFO] {seconds}초 대기 중...")
    time.sleep(seconds)
    
  