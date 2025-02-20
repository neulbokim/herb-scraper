# modules/utils/data_utils.py

import json
import pandas as pd
import os
from modules.utils.logger import setup_logger

logger = setup_logger("data_utils")


def load_from_json(file_path: str):
    """📥 JSON 파일 로드"""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        logger.info(f"✅ JSON 로드 완료 → {file_path}")
        return data
    except Exception as e:
        logger.error(f"❌ JSON 로드 실패: {file_path} | {e}")
        return None


def save_to_json(data: list, file_path: str):
    """💾 JSON 파일 저장"""
    try:
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        logger.info(f"✅ JSON 저장 완료 → {file_path}")
    except Exception as e:
        logger.error(f"❌ JSON 저장 실패: {file_path} | {e}")


def load_csv(file_path: str):
    """📥 CSV 파일 로드"""
    try:
        df = pd.read_csv(file_path)
        logger.info(f"✅ CSV 로드 완료 → {file_path}")
        return df
    except Exception as e:
        logger.error(f"❌ CSV 로드 실패: {file_path} | {e}")
        return pd.DataFrame()


def save_to_csv(df: pd.DataFrame, file_path: str):
    """💾 CSV 파일 저장"""
    try:
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        df.to_csv(file_path, index=False, encoding="utf-8-sig")
        logger.info(f"✅ CSV 저장 완료 → {file_path}")
    except Exception as e:
        logger.error(f"❌ CSV 저장 실패: {file_path} | {e}")


def save_to_excel(df: pd.DataFrame, file_path: str):
    """💾 Excel 파일 저장"""
    try:
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        df.to_excel(file_path, index=False, engine="openpyxl")
        logger.info(f"✅ Excel 저장 완료 → {file_path}")
    except Exception as e:
        logger.error(f"❌ Excel 저장 실패: {file_path} | {e}")
