# modules/preprocessors/target_mapping.py

from modules.utils import load_from_json, save_to_json, setup_logger
import os

logger = setup_logger("target_mapping")

def map_targets_to_ingredients(
    ingredient_file: str,
    target_file: str,
    output_file: str = None,
    output_dir: str = None
):
    """
    🎯 성분 데이터에 타겟 단백질 매핑

    Args:
        ingredient_file (str): 입력 성분 JSON 파일 경로
        target_file (str): 타겟 단백질 JSON 파일 경로
        output_file (str): 출력 JSON 파일명 (기본: 자동 생성)
        output_dir (str): 출력 디렉토리 (기본: ingredient_file 경로)
    """
    logger.info(f"🚀 타겟 매핑 시작: {ingredient_file} + {target_file}")

    ingredients = load_from_json(ingredient_file)
    targets = load_from_json(target_file)

    if not ingredients or not targets:
        logger.error("❌ 입력 데이터 중 하나가 비어있습니다.")
        return

    for ingredient in ingredients:
        ingredient_name = ingredient.get("ingredient")
        ingredient_targets = [
            t for t in targets if t.get("ingredient") == ingredient_name
        ]
        ingredient["targets"] = ingredient_targets

    base_name = f"mapped_{os.path.splitext(os.path.basename(ingredient_file))[0]}"
    output_dir = output_dir or os.path.dirname(ingredient_file)
    os.makedirs(output_dir, exist_ok=True)
    output_file = output_file or f"{base_name}.json"
    output_path = os.path.join(output_dir, output_file)

    save_to_json(ingredients, output_path)
    logger.info(f"✅ 타겟 매핑 완료: {len(ingredients)}개 성분 → {output_path}")
