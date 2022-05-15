import os
from subprocess import Popen, PIPE
from selenium import webdriver
from time import sleep
import argparse


abspath = lambda *p: os.path.abspath(os.path.join(*p))
ROOT = abspath(os.path.dirname(__file__))


def execute_command(command):
    result = Popen(command, shell=True, stdout=PIPE).stdout.read()
    if len(result) > 0 and not result.isspace():
        raise Exception(result)


def do_screen_capturing(url, screen_path, width, height):
    print("Capturing screen..")
    chrome_options = webdriver.ChromeOptions()
    chrome_options.headless = True
    driver = webdriver.Chrome(options=chrome_options)
    #driver.set_script_timeout(15000)
    #driver.implicitly_wait(15000)
    #driver.set_page_load_timeout(15000)
    if width and height:
        driver.set_window_size(width, height)
    driver.get(url)
    sleep(60)
    driver.save_screenshot(screen_path)
    driver.quit()


def do_crop(params):
    print("Croping captured image..")
    command = [
        'convert',
        params['screen_path'],
        '-crop', '%sx%s+0+0' % (params['width'], params['height']),
        params['crop_path']
    ]
    execute_command(' '.join(command))


def do_thumbnail(params):
    print(f"Generating {params['thumbnail_path']} from cropped captured image..")
    command = [
        'convert',
        params['crop_path'],
        '-filter', 'Lanczos',
        '-thumbnail', '%sx%s' % (params['width'], params['height']),
        params['thumbnail_path']
    ]
    execute_command(' '.join(command))


def get_screen_shot(**kwargs):
    url = kwargs['url']
    width = int(kwargs.get('width', 1024))  # screen width to capture
    height = int(kwargs.get('height', 768))  # screen height to capture
    # file name e.g. screen.png
    filename = kwargs.get('filename', 'screen.png')
    path = kwargs.get('path', ROOT)  # directory path to store screen

    crop = kwargs.get('crop', False)  # crop the captured screen
    crop_width = int(kwargs.get('crop_width', width)
                     )  # the width of crop screen
    crop_height = int(kwargs.get('crop_height', height)
                      )  # the height of crop screen
    # does crop image replace original screen capture?
    crop_replace = kwargs.get('crop_replace', False)

    # generate thumbnail from screen, requires crop=True
    thumbnail = kwargs.get('thumbnail', False)
    # the width of thumbnail
    thumbnail_width = int(kwargs.get('thumbnail_width', width))
    # the height of thumbnail
    thumbnail_height = int(kwargs.get('thumbnail_height', height))
    # does thumbnail image replace crop image?
    thumbnail_replace = kwargs.get('thumbnail_replace', False)

    screen_path = abspath(path, filename)
    crop_path = thumbnail_path = screen_path

    if thumbnail and not crop:
        raise Exception(
            'Thumnail generation requires crop image, set crop=True')

    do_screen_capturing(url, screen_path, width, height)

    if crop:
        if not crop_replace:
            crop_path = abspath(path, 'crop_'+filename)
        params = {
            'width': crop_width, 'height': crop_height,
            'crop_path': crop_path, 'screen_path': screen_path}
        do_crop(params)

        if thumbnail:
            if not thumbnail_replace:
                thumbnail_path = abspath(path, 'thumbnail_'+filename)
            params = {
                'width': thumbnail_width, 'height': thumbnail_height,
                'thumbnail_path': thumbnail_path, 'crop_path': crop_path}
            do_thumbnail(params)
    return screen_path, crop_path, thumbnail_path


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Work on screenshots')
    parser.add_argument('--id', help='Enter ID', required=True)
    args = parser.parse_args()

    id = args.id

    url = f'https://brainsharer.org/ng/?id={id}'
    screen_path, crop_path, thumbnail_path = get_screen_shot(
        url=url, filename= f'{id}.png',
        crop=True, crop_replace=False,
        thumbnail=True, thumbnail_replace=False,
        thumbnail_width=200, thumbnail_height=150,
    )
