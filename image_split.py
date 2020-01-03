from PIL import Image, ImageOps
import os, sys

left_arr, up_arr, right_arr, low_arr = [], [], [], []
# Set default format
img_format = '.png'


def create_dir(dir_name):
    print('Creating file directory...')
    if not os.path.exists(dir_name):
        try:
            os.makedirs(dir_name)
        except OSError:
            print('Error creating ' + dir_name)


def cut(cut_arr, image, img_format):
    print('Cropping...')

    # Checks if the path includes a folder or not
    if '/' not in image.filename:
        path = './' + os.path.splitext(image.filename)[0]
    else:
        path = './' + os.path.splitext(os.path.split(image.filename)[1])[0]

    create_dir(path)
    img_num = 1
    for cut in cut_arr:
        # Crops further incase there are mistakes in the cut
        img = image.crop(cut)
        # invert function only works with regular RGB
        convert_img = img.convert('RGB')
        invert = ImageOps.invert(convert_img)
        new_img = ImageOps.invert(invert.crop(invert.getbbox()))

        # Checks for blank cuts
        if not ImageOps.invert(new_img).getbbox():
            pass
        else:
            new_img.save(path
                         + '/'
                         + os.path.splitext(os.path.split(image.filename)[1])[0]
                         + str(img_num)
                         + img_format)
            img_num += 1
    print('Finished!')


def create_tuple(left_arr, up_arr, right_arr, low_arr):
    cut_arr = []
    vertical = 0
    # Assigns each vertical pair with a horizontal pair 
    while vertical < len(up_arr):
        for x in range(len(left_arr)):
            cut_tuple = (left_arr[x], up_arr[vertical],
                         right_arr[x], low_arr[vertical])
            cut_arr.append(cut_tuple)
        vertical += 1
    return cut_arr


def transparent(image, data):
    print('Processing...')
    width, height = image.size
    row_num = col_num = i = j = 0
    left = upper = right = lower = int()
    # Used incase there are more than 1 pix gap for upper bound
    row_detect = col_detect = end_search = False

    while col_num <= width - 1 and row_num <= height - 1:
        # (left, *upper, right, *lower)      
        if i <= width - 1:
            if data[i + (width * row_num)] is not 0:
                row_num += 1
                i = 0
                row_detect = True
            elif i == width - 1 and not row_detect:
                i = 0
                upper += 1
                row_num += 1
            elif i == width - 1 and row_detect:
                lower = row_num

                low_arr.append(lower)
                up_arr.append(upper)

                # Start new search here instead of the beginning
                upper = row_num

                row_num += 1
                row_detect = False
                i = 0
                continue
            else:
                i += 1

        # (*left, upper, *right, lower)
        if j <= height - 1:
            if data[col_num + (j * width)] is not 0:
                col_num += 1
                j = 0
                col_detect = True
            elif j == height - 1 and not col_detect:
                j = 0
                col_num += 1
                left += 1
            elif j == height - 1 and col_detect:
                right = col_num

                left_arr.append(left)
                right_arr.append(right)

                left = col_num

                col_num += 1
                col_detect = False
                j = 0
                continue
            else:
                j += 1
    else:
        arr = create_tuple(left_arr, up_arr,
                           right_arr, low_arr)
        cut(arr, image, img_format)


# Checks for valid user input and arguments
try:
    if len(sys.argv) > 1:
        try:
            image = Image.open('%s' % sys.argv[1])
        except FileNotFoundError:
            sys.exit('Image not found')

        if len(sys.argv) > 2:
            try:
                if '.' not in sys.argv[2]:
                    img_format = '.' + sys.argv[2]
                elif sys.argv[2].find('.') == 0:
                    img_format = sys.argv[2]
                else:
                    raise RuntimeError
            except RuntimeError:
                sys.exit('Invalid Image Format')
    else:
        raise RuntimeError
except RuntimeError:
    sys.exit('No commands inputted')
except FileNotFoundError:
    sys.exit('The file could not be found')


pixels = image.convert('RGBA')
data = list(pixels.getdata(3))  # Only gets Alpha Channels
transparent(image, data)
