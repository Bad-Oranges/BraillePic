import numpy as np
import cv2
from functools import reduce
from icecream import ic
np.set_printoptions(threshold=np.inf, linewidth=np.inf)


def process_img(url, width=20, tile_size=(5, 3)):
    img = cv2.imread(url, flags=0)
    img_height, img_width = img.shape
    resize_width = width * tile_size[1]
    resize_height = int((img_height * resize_width / img_width) / 5) * 5
    img = cv2.resize(img, (resize_width, resize_height), interpolation=cv2.INTER_NEAREST)
    ret, img = cv2.threshold(img, 80, 255, cv2.THRESH_BINARY_INV)
    img[img > 0] = 1
    return img2braille(img)


def img2braille(img, tile_size=(5, 3)):
    output = ''
    for tile_lines in pic2tile(img, tile_size):
        for tile in tile_lines:
            output += tile2braille(tile)
        output += '\n'
    return output


def pic2tile(pic, tile_size=(5, 3)):
    # 将图片分成(5, 3)的tile
    img_size = pic.shape
    tile_list = np.split(pic, img_size[0]//tile_size[0], axis=0)
    for i, sub_list in enumerate(tile_list):
        tile_list[i] = np.split(sub_list, img_size[1]//tile_size[1], axis=1)
    return tile_list


def tile2braille(tile):
    # 将tile分割，转换成16进制code
    part_1 = tile[:3, 0]
    part_2 = tile[:3, 1]
    part_3 = tile[3, :2]
    new_array = reduce(lambda a, b: np.append(a, b), (part_1, part_2, part_3))
    binary_str = ''
    for i in new_array:
        binary_str = str(i) + binary_str
    code = 0x2800 + int(binary_str, base=2)
    return chr(code)
