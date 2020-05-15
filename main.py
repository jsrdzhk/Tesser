'''
@Author: Rodney Cheung
@Date: 2020-05-13 10:58:02
@LastEditors: Rodney Cheung
@LastEditTime: 2020-05-15 18:09:00
@FilePath: /Tesser/main.py
'''
import tesserocr
from tesserocr import PyTessBaseAPI, RIL
from PIL import Image, ImageOps
import os
import argparse

TESSDATA_PATH = '/Volumes/code/open_source/tessdata_best/'
# TESTDATA_PATH = '/Volumes/code/work/wq_maintain_material/picture/test_data'

print(tesserocr.tesseract_version())
print(tesserocr.get_languages(path=TESSDATA_PATH))


def str2bool(v):
    if isinstance(v, bool):
        return v
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')


def main():
    parser = argparse.ArgumentParser(description='tesserocr interface')
    parser.add_argument('-I',
                        '--invert',
                        default=False,
                        const=True,
                        nargs='?',
                        type=str2bool,
                        help='Specify whether to invert image before ocr',
                        dest='is_invert_image')
    parser.add_argument('-i',
                        '--input-img',
                        default=None,
                        type=str2bool,
                        help='Specify image to apply ocr',
                        dest='img_path')
    parser.add_argument('-d',
                        '--directory',
                        default=None,
                        type=str,
                        help='Specify directry to apply ocr for images on it',
                        dest='img_dir')
    args = parser.parse_known_args()[0]
    if args.img_dir == None and args.img_path == None:
        print("You must specify image dir or image path")
        return

    run(args.is_invert_image, args.img_path, args.img_dir)


def ocr(tess_api, img_path):
    base_name, ext = filename_component(img_path)
    if 'txt' in ext:
        return
    result_path = base_name + '.txt'
    with open(result_path, 'w') as result:
        imgHandle = Image.open(img_path)
        tess_api.SetImage(imgHandle)
        result.write(tess_api.GetUTF8Text())
        result.write('word confidence:{}\n'.format(
            tess_api.AllWordConfidences()))


def png_to_jpeg(src):
    img = Image.open(src)
    base, _ = filename_component(src)
    rgb_img = img.convert('RGB')
    new_name = base + '.jpg'
    rgb_img.save(new_name)
    return new_name


def filename_component(file_name):
    file_name_components = os.path.splitext(file_name)
    base_name = file_name_components[0]
    extension = file_name_components[-1]
    return base_name, extension


def image_invert(src, dst, quality):
    _, ext = filename_component(src)
    if 'png' in ext:
        src = png_to_jpeg(src)
    img = Image.open(src)
    img_invert = ImageOps.invert(img)
    img_invert.save(dst, quality=quality)


def pretreatment(is_invert_image, src_image_path):
    _, ext = filename_component(src_image_path)
    if 'txt' in ext:
        return
    pretreatment_imgs = list()
    if is_invert_image:
        base, ext = filename_component(src_image_path)
        inverted_image_path = base + '_inverted' + ext
        image_invert(src_image_path, inverted_image_path, 95)
        pretreatment_imgs.append(inverted_image_path)
    return pretreatment_imgs


def run(is_invert_image=False, image_path=None, image_dir=None):
    with PyTessBaseAPI(path=TESSDATA_PATH, lang='chi_sim') as api:
        if image_dir != None:
            for home, _, files in os.walk(image_dir):
                for f in files:
                    if f == '.DS_Store':
                        continue
                    img = os.path.join(home, f)
                    print(img)
                    pretreatment_imgs = pretreatment(is_invert_image, img)
                    ocr(api, img)
                    for pretreatment_img in pretreatment_imgs:
                        ocr(api, pretreatment_img)
        if image_path != None:
            pretreatment_imgs = pretreatment(is_invert_image, image_path)
            ocr(api, image_path)
            for pretreatment_img in pretreatment_imgs:
                ocr(api, pretreatment_img)


if __name__ == "__main__":
    main()