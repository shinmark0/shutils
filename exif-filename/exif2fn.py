# This code renames original filename to datetime format
# using datetime in image exif.
# It needs below:
# > pip install image

import datetime
import os

import PIL
from PIL import Image

def exifToFilename(filename):

    decoder = "%Y:%m:%d %H:%M:%S"
    encoder = "%Y%m%d-%H%M%S"

    purefn, ext = os.path.splitext(filename) 

    with Image.open(filename) as image:
        info = image._getexif()
        exifdatestr = info[36867]
        dt = datetime.datetime.strptime(exifdatestr, decoder)
        renamedstr = datetime.datetime.strftime(dt, encoder)

        resultfn = renamedstr + ext

        # Windows 에서는 변경할 파일명으로 파일이 이미 존재하면 예외가 발생하므로 별도 확인이 필요 없으나
        # Unix 에서는 이미 파일이 존재해도 덮어써버리기 때문에 반드시 사전확인이 필요하다.
        if os.path.isfile(resultfn):
            print("failed to rename: [" + resultfn + "] already exists.")
        else:
            os.rename(filename, resultfn)
            print("rename: [" + filename + "] to [" + resultfn + "]")
            
    return


count = 0

while True:
    try:
        filename = input()
        exifToFilename(filename)
        count = count + 1
    except EOFError:
        break
    #except PIL.UnidentifiedImageError:
    except:
        print("exif read failed: [" + filename + "]")


print(str(count) + " files are renamed.")
