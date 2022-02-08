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
