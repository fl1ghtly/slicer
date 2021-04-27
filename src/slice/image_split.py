from PIL import Image, ImageOps
from queue import LifoQueue
import os
import sys
import time
import itertools
import threading
import argparse


def create_dir(dir_name):
    print("Making Directory...")
    if not os.path.exists(dir_name):
        try:
            os.makedirs(dir_name)
        except OSError:
            print('Error creating ' + dir_name)


def find_path(img):
    if '/' not in img.filename:
        path = './' + os.path.splitext(img.filename)[0]
    else:
        path = './' + os.path.splitext(os.path.split(img.filename)[1])[0]
    return path


def save_image(new_img, original_img, img_num, path, img_format):
    new_img.save(path
                 + '/'
                 + os.path.splitext(
                     os.path.split(original_img.filename)[1])[0]
                 + str(img_num)
                 + img_format)


# Repeatedly shows ... in sequence
def show_progress():
    progress_thread = threading.currentThread()
    load_str = ''
    while getattr(progress_thread, "is_loading", True):
        if len(load_str) >= 3:
            load_str = ''
            # Clears last printed line
            sys.stdout.write("\033[K")
        else:
            load_str += '.'
        print(load_str, end='\r')
        time.sleep(0.2)


def create_new_image(bottom_right_pt, new_coords, transform, image, img_format):
    channel = 'RGBA'
    if img_format == '.jpg':
        channel = 'RGB'

    im = Image.new(
        channel, (bottom_right_pt[0] + 1, bottom_right_pt[1] + 1), (0, 0, 0, 0))
    for point in new_coords:
        im.putpixel(point, image.getpixel(transform.get(point)))
    return im


# Returns list of points in a shape
def expand_search(point, memo, coord_dictionary):
    stack = LifoQueue()
    stack.put(point)
    while(not stack.empty()):
        point = stack.get(point)

        relative_pts = [(point[0] - 1, point[1] + 1), (point[0], point[1] + 1),
                        (point[0] + 1, point[1] + 1), (point[0] - 1, point[1]),
                        (point[0] + 1, point[1]), (point[0] - 1, point[1] - 1),
                        (point[0], point[1] - 1), (point[0] + 1, point[1] - 1)]

        memo.add(point)
        coord_dictionary.update({point: 0})
        for i in range(8):
            if relative_pts[i] not in memo and coord_dictionary.get(relative_pts[i]) is not None:
                if coord_dictionary.get(relative_pts[i]) > 0:
                    stack.put(relative_pts[i])

    return memo


# Creates a dictionary with a point and its associated alpha value
def create_coordinates(data, width, height):
    print("Mapping Coordinates...")
    # dict {(x,y) : alpha value}
    coordinate_dic = {}
    cur_width = 0
    cur_height = 0

    for point in data:
        if cur_height < height:
            if cur_width < width:
                coordinate_dic.update({(cur_width, cur_height): point})
                cur_width += 1
            else:
                cur_width = 0
                cur_height += 1
                coordinate_dic.update({(cur_width, cur_height): point})
                cur_width += 1

    return coordinate_dic


# Transforms coordinate position to have their starting position at (0, 0)
def normalize_coordinates(top_left_bound, bottom_right_bound, set_of_coords):
    new_set = set()
    transform_map = {}

    x_transform = top_left_bound[0]
    y_transform = top_left_bound[1]

    new_bottom_right = [bottom_right_bound[0], bottom_right_bound[1]]

    new_bottom_right[0] -= x_transform
    new_bottom_right[1] -= y_transform

    for coord in set_of_coords:
        new_coord = (coord[0] - x_transform, coord[1] - y_transform)
        new_set.add(new_coord)
        transform_map.update({new_coord: coord})

    return transform_map, tuple(new_bottom_right), new_set


# Finds the first instance of an opaque pixel
def find_point(width, height, coord_dictionary):
    point = None
    for y in range(height):
        for x in range(width):
            if coord_dictionary.get((x, y)) > 0:
                point = (x, y)
                return point

    # Point is None in this case
    return point


def find_x_bounds(coord_set):
    min_x = list(coord_set)[0][0]
    max_x = list(coord_set)[0][0]

    for point in coord_set:
        if point[0] > max_x:
            max_x = point[0]

        if point[0] < min_x:
            min_x = point[0]

    return min_x, max_x


def find_y_bounds(coord_set):
    min_y = list(coord_set)[0][1]
    max_y = list(coord_set)[0][1]

    for point in coord_set:
        if point[1] > max_y:
            max_y = point[1]

        if point[1] < min_y:
            min_y = point[1]

    return min_y, max_y


def calculate_bounding_points(x_min, y_min, x_max, y_max):
    # Top Left, Bottom Right
    return (x_min, y_min), (x_max, y_max)


def remove_points(coord_list, coord_dict):
    for point in coord_list:
        coord_dict.update({point: 0})


def slice_image(img_num, start, coord_map, converted_image, original_image, path, img_format):
    # memo_bound is a set because lookup is O(1) instead of list O(n)
    memo_bound = set()

    thread = threading.Thread(target=show_progress)
    thread.start()
    expand_search(start, memo_bound, coord_map)
    thread.is_loading = False

    min_x_bound, max_x_bound = find_x_bounds(memo_bound)
    min_y_bound, max_y_bound = find_y_bounds(memo_bound)

    top_left, bottom_right = calculate_bounding_points(min_x_bound,
                                                       min_y_bound,
                                                       max_x_bound,
                                                       max_y_bound)

    translation_map, norm_bottom_right, norm_coords = normalize_coordinates(top_left,
                                                                            bottom_right,
                                                                            memo_bound)

    img_slice = create_new_image(
        norm_bottom_right, norm_coords, translation_map, converted_image, img_format)
    save_image(img_slice, original_image, img_num, path, img_format)
    remove_points(memo_bound, coord_map)


def start_slice():
    # Checks for valid user input and arguments
    parser = argparse.ArgumentParser(
        description='Slices clusters of pixels into separate images')
    parser.add_argument('image', metavar='i', type=str,
                        help='Path to image. Must include file extension')
    parser.add_argument(
        '-t', help='What file type each image should be saved as', nargs='?', default='.png')
    args = parser.parse_args()

    # Sets Default image format
    img_format = args.t

    try:
        try:
            orig_image = Image.open('%s' % args.image)
            print("Starting...")
        except FileNotFoundError:
            sys.exit('Image not found')
        try:
            if '.' not in args.t:
                img_format = '.' + args.t
            elif args.t.find('.') == 0:
                img_format = args.t
            else:
                raise RuntimeError
        except RuntimeError:
            sys.exit('Invalid Image Format')
    except RuntimeError:
        sys.exit('No commands inputted')
    except FileNotFoundError:
        sys.exit('The file could not be found')

    pixels = orig_image.convert('RGBA')
    data = list(pixels.getdata(3))

    width_img, height_img = orig_image.size
    # Only gets Alpha Channels
    coord_dic = create_coordinates(data, width_img, height_img)
    filepath = find_path(orig_image)

    create_dir(filepath)
    img_count = 1

    print("Starting Slice...")
    start_point = find_point(width_img, height_img, coord_dic)

    while start_point is not None:
        slice_image(img_count, start_point, coord_dic,
                    pixels, orig_image, filepath, img_format)
        img_count += 1
        start_point = find_point(width_img, height_img, coord_dic)

    print("Finished!")


if __name__ == '__main__':
    start_slice()
