from urllib.request import urlretrieve
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import imageio

TXT_FILE = 'images.txt'
BUFFER_FILE = 'Buffer.txt'
LABEL_FILE = 'labels.txt'
URL_FILE = 'urls.txt'
IMG_SIZE = (125, 40)


def get_all_urls():
    with open(URL_FILE, 'r') as urlr:
        urls = urlr.readlines()
    for url in urls:
        yield url


print('executed')
