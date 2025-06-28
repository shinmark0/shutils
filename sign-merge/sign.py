# author: chatGPT4o
# designer: shinmark0
# 이미지에 사인 입히는 툴입니다. 그림에 사인 넣거나 사진에 스탬프 박아넣는 용도로 쓸만합니다.
# Sign stamp tool on image. Useful for draw sign or stamp on photo.

import argparse
from PIL import Image
import os

POSITION_MAP = {
    'T': 'top',
    'C': 'center',
    'B': 'bottom',
    'L': 'left',
    'R': 'right'
}

def calculate_position(base_size, overlay_size, position_code):
    """
    기준 이미지 위에 서명을 배치할 좌표(x, y)를 계산하는 함수
    
    base_size: 기준 이미지 크기 (width, height)
    overlay_size: 서명 이미지 크기 (width, height)
    position_code: 위치 코드 (예: 'BR', 'CC')
    """
    base_w, base_h = base_size
    overlay_w, overlay_h = overlay_size

    vertical = POSITION_MAP.get(position_code[0], 'bottom')
    horizontal = POSITION_MAP.get(position_code[1], 'right')

    if vertical == 'top':
        y = 0
    elif vertical == 'center':
        y = (base_h - overlay_h) // 2
    else:  # bottom
        y = base_h - overlay_h

    if horizontal == 'left':
        x = 0
    elif horizontal == 'center':
        x = (base_w - overlay_w) // 2
    else:  # right
        x = base_w - overlay_w

    return x, y

def apply_signature(original_path, sign_path, position_code, scale, quality):
    """
    원본 이미지에 서명을 덧입히는 함수

    original_path: 원본 이미지 경로
    sign_path: 서명 이미지 경로
    position_code: 위치 코드 (예: 'BR')
    scale: 서명 크기 비율 (기준 너비 대비)
    quality: 저장 품질 (0~100)
    """
    base_img = Image.open(original_path).convert("RGBA")
    sign_img = Image.open(sign_path).convert("RGBA")

    # 기준이 되는 축 길이 계산
    base_w, base_h = base_img.size
    min_side = min(base_w, base_h)
    target_size = int(min_side * scale)

    # 비율 유지한 채로 리사이징
    sign_w, sign_h = sign_img.size
    ratio = sign_w / sign_h
    if sign_w > sign_h:
        new_w = target_size
        new_h = int(target_size / ratio)
    else:
        new_h = target_size
        new_w = int(target_size * ratio)
    sign_img = sign_img.resize((new_w, new_h), Image.LANCZOS)

    # 위치 계산
    if len(position_code) != 2:
        position_code = "BR"
    x, y = calculate_position(base_img.size, sign_img.size, position_code.upper())

    # 합성
    result = base_img.copy()
    result.paste(sign_img, (x, y), sign_img)

    # 저장 경로 생성 (항상 jpg, _signed 붙이기)
    base_name = os.path.splitext(original_path)[0]
    output_path = f"{base_name}_signed.jpg"

    # JPG 저장 with quality and optimize
    rgb_result = result.convert("RGB")
    rgb_result.save(output_path, format="JPEG", quality=quality, optimize=True)
    print(f"✔ 저장 완료: {output_path} (퀄리티 {quality}, optimize=True)")

def main():
    parser = argparse.ArgumentParser(description="이미지에 사인 추가 툴")
    parser.add_argument('-i', '--image', required=True, help='원본 이미지 경로')
    parser.add_argument('-s', '--sign', required=True, help='사인 이미지 경로')
    parser.add_argument('-p', '--position', default='BR', help='사인 위치 (예: TL, CC, BR)')
    parser.add_argument('-sc', '--scale', type=float, default=0.1, help='사인 스케일 (0~1)')
    parser.add_argument('-q', '--quality', type=int, default=95, help='JPG 저장 퀄리티 (1~100)')

    args = parser.parse_args()
    apply_signature(args.image, args.sign, args.position.upper(), args.scale, args.quality)

if __name__ == "__main__":
    main()