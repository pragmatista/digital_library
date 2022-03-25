import numpy as np
import cv2
import pytesseract as pt
from PIL import Image
import sqlite3
sqlite3.register_adapter(np.int64, lambda val: int(val))


def calculate_compare_score(filepath, compression=100, size=0):
    # Function that searches the folder for image files, converts them to a matrix;
    # the sum of the matrix values give us a score that could be used to find
    # duplicate files (with an exact score match)
    try:
        image = decode_image(filepath, compression)
        return np.sum(np.array(image)).astype(np.int64)
    except:
        return size


def decode_image(filepath, compression=100):
    # create images matrix
    try:
        img = cv2.imdecode(np.fromfile(filepath, dtype=np.uint8), cv2.IMREAD_UNCHANGED)
        if type(img) == np.ndarray:
            img = img[..., 0:3]
            img = cv2.resize(img, dsize=(compression, compression), interpolation=cv2.INTER_CUBIC)
        return img
    except:
        return 0


def mse(imageA, imageB):
    try:
        err = np.sum((imageA.astype("float") - imageB.astype("float")) ** 2)
        err /= float(imageA.shape[0] * imageA.shape[1])
        return err
    except:
        return None


# TODO: finish developing method to parse text by extending the fso output
def extract_text_from_image(path: str):
    # Converting image to text
    img = Image.open(path)
    extracted = pt.image_to_string(img)

    return extracted if extracted.strip() else None

    # results = []
    # if extracted.strip():
    #     data = {
    #         'search'
    #     }


    # if extracted.strip():
    #     fso = FileSystemObject(path).to_dict()
    #     fso['extracted_text'] = extracted.strip()
    #     return fso
    # else:
    #     return None


    # output = []
    # for result in results:
    #     file = list(result.split(":"))
    #     fso = FileSystemObject(file[0]).to_dict()
    #     fso['search'] = text
    #     fso['text_found'] = file[2]
    #     fso['page_num'] = file[1]
    #     output.append(fso)
    #
    # return output

