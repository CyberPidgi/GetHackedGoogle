from __init__ import *
IMG_FILENAME = 'reCAPTCHA image.png'


def clear(file):
    # temporary function
    # delete later
    open(file, 'w').close()


def convert_rgb_to_black(rgb):
    """

    :param rgb: array of the image
    :return: grayscale of the array
    converts the array passed in to a greyscale 2D array
    """
    # wtf is this syntax
    # ... =  remaining dimensions in an array
    return np.dot(rgb[..., :3], [0.299, 0.587, 0.114])


def get_image(url=None, filename=None):
    global IMG_FILENAME
    IMG_FILENAME = 'reCAPTCHA image.png'
    if filename:
        IMG_FILENAME = filename
    elif url:
        urlretrieve(url, IMG_FILENAME)
    else:
        raise ValueError('Give at least one parameter')


def find_black_pixels(image):
    black_x_pixels, black_y_pixels = [], []
    colour_threshold = 3

    for y, row in enumerate(image):
        for x, rgb_val in enumerate(row):
            if rgb_val < colour_threshold:
                black_x_pixels.append(x)
                black_y_pixels.append(y)

    return black_x_pixels, black_y_pixels


def find_greatest_area_of_black_pixels(black_x_pixels, black_y_pixels):
    dict_index = 1
    dist_threshold = 20
    sorting_dict = {}
    sorting_list = []
    black_pxl_list_len = len(black_x_pixels)

    # find groups of black pixels and sorts them into a dictionary, with the indices being a number
    print('STARTING SORT')
    for index in range(black_pxl_list_len - 1):
        x, y = black_x_pixels[index], black_y_pixels[index]
        sorting_list.append((x, y))
        if black_x_pixels[index + 1] - black_x_pixels[index] > dist_threshold or \
                black_y_pixels[index + 1] - black_y_pixels[index] > dist_threshold:
            sorting_dict[str(dict_index)] = tuple(sorting_list)
            dict_index += 1
            sorting_list = []
    print(f'ENDED SORT \nThe dictionary is {len(sorting_dict)} indices long.')

    # find the biggest group
    greatest_len = [0, '0']
    for num in sorting_dict.keys():
        if greatest_len[0] < len(sorting_dict[num]):
            greatest_len[0], greatest_len[1] = len(sorting_dict[num]), num

    # decode the lists
    x_list, y_list = [], []
    for x, y in sorting_dict[greatest_len[1]]:
        x_list.append(x)
        y_list.append(y)
    return x_list, y_list


def find_text(image):
    """

    :param image: the requested image as an array has to be passed in
    :return: the cropping region's bounds

    The function finds the text in a reCAPTCHA image.It does struggle if the image has two
    or more texts, as you find the text using the region that has the most amount of black pixels to determine the
    the text area.
    """
    black_x_pixels, black_y_pixels = find_black_pixels(image)
    x_list, y_list = find_greatest_area_of_black_pixels(black_x_pixels, black_y_pixels)

    # offset the crop
    offset_x, offset_y = 20, 15  # 20, 4
    min_x, max_x = min(x_list) - offset_x, max(x_list) + offset_x
    min_y, max_y = min(y_list) - offset_y, max(y_list) + offset_y
    return min_x, min_y, max_x, max_y


def format_image():
    # convert the image to greyscale
    pic = imageio.imread(IMG_FILENAME)
    grey_pic = convert_rgb_to_black(pic)

    # gets the rectangular region bounding the text
    crop_args = find_text(grey_pic)

    # crops using the coordinates of the rectangular region
    img = Image.open(IMG_FILENAME)
    img = img.crop(crop_args)
    img = img.resize(IMG_SIZE, Image.ANTIALIAS)  # resize to make it all of equal length
    img.save(IMG_FILENAME, quality=100)


def append_image_to_file(file=None):
    array = imageio.imread(IMG_FILENAME)
    array = convert_rgb_to_black(array)  # converts it to 2D array

    np.savetxt(BUFFER_FILE, array)
    txt_file = file or TXT_FILE
    with open(txt_file, 'a') as tf:
        with open(BUFFER_FILE, 'r') as bf:
            for txt in bf.readlines():
                tf.write(txt)
            tf.write(';\n')
    clear(BUFFER_FILE)


def read_images_from_file(file=None):
    txt_file = file or TXT_FILE
    tf = open(txt_file, 'r')
    bf = open(BUFFER_FILE, 'w')
    labels = read_labels_from_file()
    for txt in tf.readlines():
        if ';' in txt:
            pic = np.genfromtxt(BUFFER_FILE)
            # print(pic.shape)
            pic = np.reshape(pic, pic.shape + (1,))
            # print(pic.shape)
            plt.figure(figsize=(5, 5))
            plt.title(f'{next(labels)}')
            plt.imshow(pic)
            plt.show()
            bf.close()
            bf = open(BUFFER_FILE, 'w')
            continue
        bf.write(txt)

    tf.close()
    bf.close()
    clear(BUFFER_FILE)
    # clear(TXT_FILE)


def read_labels_from_file(file=None):
    label_file = file or LABEL_FILE
    with open(label_file, 'r') as lf:
        return (label for label in lf.readlines())


def main():
    clear(TXT_FILE)
    for num, url in enumerate(get_all_urls(), 1):
        print(f'\n{num}')
        get_image(url)
        format_image()
        append_image_to_file()
    read_images_from_file()


if __name__ == '__main__':
    main()
