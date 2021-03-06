# -*- coding: utf-8 -*-

"""

    use adb to capture the phone screen
    then use hanwang text recognize the text
    then use baidu to search answer

"""

import os
import platform
import subprocess
import sys
from common import wda
from datetime import datetime
from shutil import copyfile

from PIL import Image
from common.config import enable_scale
# SCREENSHOT_WAY 是截图方法，
# 经过 check_screenshot 后，会自动递
# 不需手动修改
SCREENSHOT_WAY = 3


def get_adb_tool():
    adb_bin = wda.Client()
    return adb_bin


def check_screenshot(filename, directory):
    """
    检查获取截图的方式
    """
    save_shot_filename = os.path.join(directory, filename)
    global SCREENSHOT_WAY
    if os.path.isfile(save_shot_filename):
        try:
            os.remove(save_shot_filename)
        except Exception:
            pass
    if SCREENSHOT_WAY < 0:
        print("暂不支持当前设备")
        sys.exit()
    capture_screen(filename, directory)
    try:
        Image.open(save_shot_filename).load()
        print("采用方式 {} 获取截图".format(SCREENSHOT_WAY))
    except Exception:
        SCREENSHOT_WAY -= 1
        check_screenshot(filename=filename, directory=directory)


def analyze_current_screen_text(crop_area, directory=".", compress_level=1, use_monitor=False):
    """
    capture the android screen now

    :return:
    """
    print("capture time: ", datetime.now().strftime("%H:%M:%S"))
    screenshot_filename = "screenshot.png"
    save_text_area = os.path.join(directory, "text_area.png")
    capture_screen_v2(screenshot_filename, directory)
    parse_answer_area(os.path.join(directory, screenshot_filename),
                      save_text_area, compress_level, crop_area)
    #return get_area_data(save_text_area)


def analyze_stored_screen_text(screenshot_filename="screenshot.png", directory=".", compress_level=1):
    """
    reload screen from stored picture to store
    :param directory:
    :param compress_level:
    :return:
    """
    save_text_area = os.path.join(directory, "text_area.png")
    parse_answer_area(os.path.join(
        directory, screenshot_filename), save_text_area, compress_level)
    return get_area_data(save_text_area)


def capture_screen_v2(filename="screenshot.png", directory="."):
    """
    can't use general fast way

    :param filename:
    :param directory:
    :return:
    """
    adb_bin = get_adb_tool()
    adb_bin.screenshot(os.path.join(directory, filename))


def capture_screen(filename="screenshot.png", directory="."):
    """
    获取屏幕截图，目前有 0 1 2 3 四种方法，未来添加新的平台监测方法时，
    可根据效率及适用性由高到低排序

    :param filename:
    :param directory:
    :return:
    """
    global SCREENSHOT_WAY
    adb_bin = get_adb_tool()
    adb_bin.screenshot(os.path.join(directory, filename))




def save_screen(filename="screenshot.png", directory="."):
    """
    Save screen for further test
    :param filename:
    :param directory:
    :return:
    """
    copyfile(os.path.join(directory, filename),
             os.path.join(directory + "/ios/", datetime.now().strftime("%m%d_%H%M%S").join(os.path.splitext(filename))))


def parse_answer_area(source_file, text_area_file, compress_level, crop_area):
    """
    crop the answer area

    :return:
    """

    image = Image.open(source_file)
    if compress_level == 1:
        image = image.convert("L")
    elif compress_level == 2:
        image = image.convert("1")

    width, height = image.size[0], image.size[1]
    print("screen width: {0}, screen height: {1}".format(width, height))
    #ak=image.fp.read()
    region = image.crop(
        (width * crop_area[0], height * crop_area[1], width * crop_area[2], height * crop_area[3]))
    if enable_scale:
        region=region.resize((int(1080/3),int(1920/5)),Image.BILINEAR)
    region.save(text_area_file)
    #image_data=region.fp.read()
    ##return image_data
    ##region.save(text_area_file)


def get_area_data(text_area_file):
    """

    :param text_area_file:
    :return:
    """
    with open(text_area_file, "rb") as fp:
        image_data = fp.read()
        return image_data
    return ""
