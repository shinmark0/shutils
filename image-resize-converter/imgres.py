# 2025.05.15.
# author: chatGPT4o
# designer: shinmark0

import argparse
import os
from PIL import Image

def normalize_format(fmt):
    fmt = fmt.lower()
    if fmt == 'jpg':
        return 'JPEG'
    elif fmt == 'png':
        return 'PNG'
    else:
        return fmt.upper()

def resize_image(source_path, target_format, quality, ratio=None, width=None, height=None):
    if not os.path.isfile(source_path):
        print(f"오류: 원본 파일 '{source_path}' 이 존재하지 않습니다.")
        return

    base_name = os.path.splitext(os.path.basename(source_path))[0]
    target_ext = target_format.lower()
    target_filename = f"{base_name}.{target_ext}"

    if os.path.exists(target_filename):
        print(f"오류: 리사이징된 파일 '{target_filename}' 이 이미 존재합니다.")
        return

    try:
        with Image.open(source_path) as img:
            original_width, original_height = img.width, img.height

            if ratio:
                new_width = int(original_width * ratio)
                new_height = int(original_height * ratio)
                print(f"비율 기준 리사이징: {original_width}x{original_height} -> {new_width}x{new_height}")
            elif width:
                new_width = width
                new_height = int((width / original_width) * original_height)
                print(f"폭 기준 리사이징: {original_width}x{original_height} -> {new_width}x{new_height}")
            elif height:
                new_height = height
                new_width = int((height / original_height) * original_width)
                print(f"높이 기준 리사이징: {original_width}x{original_height} -> {new_width}x{new_height}")
            else:
                new_width, new_height = original_width, original_height
                print(f"리사이즈 없이 포맷만 변경: {original_width}x{original_height}")

            resized_img = img.resize((new_width, new_height), Image.LANCZOS) if (new_width != original_width or new_height != original_height) else img

            save_options = {}
            normalized_format = normalize_format(target_format)

            if normalized_format == 'JPEG':
                save_options['quality'] = quality
                save_options['optimize'] = True
            elif normalized_format == 'PNG':
                save_options['optimize'] = True
                if quality != 100:
                    print("알림: PNG 포맷은 '-q' 옵션을 무시합니다.")
            else:
                print(f"주의: '{target_format}' 포맷은 별도 압축 옵션 없이 저장됩니다.")

            resized_img.save(target_filename, format=normalized_format, **save_options)
            print(f"성공: '{target_filename}' 로 저장되었습니다.")
    except Exception as e:
        print(f"오류 발생: {e}")

def main():
    parser = argparse.ArgumentParser(description='이미지를 리사이징 및 포맷 변경하는 스크립트')
    parser.add_argument('-s', '--source', required=True, help='원본 이미지 파일명')
    parser.add_argument('-r', '--ratio', type=float, help='리스케일 비율 (예: 0.5, 2)')
    parser.add_argument('-W', '--width', type=int, help='목표 폭 (px)')
    parser.add_argument('-H', '--height', '-e', type=int, help='목표 높이 (px)')
    parser.add_argument('-f', '--format', required=True, help='저장할 포맷 (예: jpg, png)')
    parser.add_argument('-q', '--quality', type=int, default=95, help='이미지 저장 품질 (기본: 95, 0~100)')

    args = parser.parse_args()

    if not (0 <= args.quality <= 100):
        print("오류: '-q' 옵션은 0~100 사이의 값이어야 합니다.")
        return

    resize_image(
        args.source,
        args.format,
        args.quality,
        ratio=args.ratio,
        width=args.width,
        height=args.height
    )

if __name__ == "__main__":
    main()