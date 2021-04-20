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


# Returns list of points in a shape
def expand_search(point, memo):
    if point not in memo and coord_dic.get(point) is not None:
        if coord_dic.get(point) > 0:
            memo.append(point)

            expand_search((point[0] - 1, point[1] + 1), memo)
            expand_search((point[0], point[1] + 1), memo)
            expand_search((point[0] + 1, point[1] + 1), memo)
            expand_search((point[0] - 1, point[1]), memo)
            expand_search((point[0] + 1, point[1]), memo)
            expand_search((point[0] - 1, point[1] - 1), memo)
            expand_search((point[0], point[1] - 1), memo)
            expand_search((point[0] + 1, point[1] - 1), memo)

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


# Finds the first instance of an opaque pixel
def find_point(width, height):
    point = None
    for y in range(height):
        for x in range(width):
            if coord_dic.get((x, y)) > 0:
                point = (x,y)
                return point
    
    # Point is None in this case
    return point


def find_x_bounds(coord_list):
    min_x = coord_list[0][0]
    max_x = coord_list[0][0]

    for point in coord_list:
        if point[0] > max_x:
            max_x = point[0]
        
        if point[0] < min_x:
            min_x = point[0]
    
    return min_x, max_x


def find_y_bounds(coord_list):
    min_y = coord_list[0][1]
    max_y = coord_list[0][1]

    for point in coord_list:
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
start_point = find_point(width_img, height_img)
if start_point is not None:
    memo_bound = []

    expand_search(start_point, memo_bound)

    min_x_bound, max_x_bound = find_x_bounds(memo_bound)
    min_y_bound, max_y_bound = find_y_bounds(memo_bound)

    # FIXME the boundry will include points that are not originally in the expand_search list
    # Must separate those points from the expand search list from the image itself, so no rogue points
    # can be cut accidently
    top_left, top_right, bottom_left, bottom_right = calculate_bounding_points(min_x_bound, 
                                                                               min_y_bound, 
                                                                               max_x_bound, 
                                                                               max_y_bound)
