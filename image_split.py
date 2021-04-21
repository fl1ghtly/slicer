from PIL import Image, ImageOps
import os, sys

# Set default format
img_format = '.png'

def create_dir(dir_name):
    print('Creating file directory...')
    if not os.path.exists(dir_name):
        try:
            os.makedirs(dir_name)
        except OSError:
            print('Error creating ' + dir_name)


def find_path():
    if '/' not in image.filename:
        path = './' + os.path.splitext(image.filename)[0]
    else:
        path = './' + os.path.splitext(os.path.split(image.filename)[1])[0]


def save_image(bound, image, path, img_num, img_format):
    crop_img = image.crop(bound)
    crop_img.save(path
                  + '/'
                  + os.path.splitext(
                        os.path.split(image.filename)[1])[0]
                  + str(img_num)
                  + img_format)

def create_new_image():
    pass


# Returns list of points in a shape
def expand_search(point, memo, coord_dictionary):
    if point not in memo and coord_dictionary.get(point) is not None:
        if coord_dictionary.get(point) > 0:
            memo.add(point)

            # Searches surrounding points
            expand_search((point[0] - 1, point[1] + 1), memo, coord_dictionary)
            expand_search((point[0], point[1] + 1), memo, coord_dictionary)
            expand_search((point[0] + 1, point[1] + 1), memo, coord_dictionary)
            expand_search((point[0] - 1, point[1]), memo, coord_dictionary)
            expand_search((point[0] + 1, point[1]), memo, coord_dictionary)
            expand_search((point[0] - 1, point[1] - 1), memo, coord_dictionary)
            expand_search((point[0], point[1] - 1), memo, coord_dictionary)
            expand_search((point[0] + 1, point[1] - 1), memo, coord_dictionary)

    return memo


# Creates a dictionary with a point and its associated alpha value
def create_coordinates(data, width, height):
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
    # FIXME might not work for images that are bigger on one side than the other
    new_set = set()

    x_transform = top_left_bound[0]
    y_transform = top_left_bound[1]

    new_top_left = (0, 0)
    new_bottom_right = [bottom_right_bound[0], bottom_right_bound[1]]

    new_bottom_right[0] -= x_transform 
    new_bottom_right[1] -= y_transform 

    for coord in set_of_coords:
        new_set.add((coord[0] - x_transform, coord[1] - y_transform))

    return new_top_left, tuple(new_bottom_right), new_set


# Finds the first instance of an opaque pixel
def find_point(width, height, coord_dictionary):
    point = None
    for y in range(height):
        for x in range(width):
            if coord_dictionary.get((x, y)) > 0:
                point = (x,y)
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
    # Top Left, Top Right, Bottom Left, Bottom Right
    return (x_min, y_min), (x_max, y_min), (x_min, y_max), (x_max, y_max)


# MAIN 
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
width_img, height_img = image.size
data = list(pixels.getdata(3))  # Only gets Alpha Channels
coord_dic = create_coordinates(data, width_img, height_img)

# TODO move into its own function

start_point = find_point(width_img, height_img, coord_dic)

if start_point is not None:
    # memo_bound is a set because lookup is O(1) instead of list O(n)
    memo_bound = set()

    expand_search(start_point, memo_bound, coord_dic)
    
    min_x_bound, max_x_bound = find_x_bounds(memo_bound)
    min_y_bound, max_y_bound = find_y_bounds(memo_bound)

    top_left, top_right, bottom_left, bottom_right = calculate_bounding_points(min_x_bound, 
                                                                               min_y_bound, 
                                                                               max_x_bound, 
                                                                               max_y_bound)
    
    new_top_left, new_bottom_right, new_memo = normalize_coordinates(top_left, bottom_right, memo_bound)

