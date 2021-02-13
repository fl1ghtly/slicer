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

# Finds the upper and lower bounds of the shape
def find_bounds(coordinate_array, direction, width, height):
    marked_points = []
    bounds = []

    if direction is "Y":
        for y in range(height):
            for x in range(width):
                if coordinate_array.get((x, y)) > 0:
                    marked_points.append(y)
    else:
        for x in range(width):
            for y in range(height):
                if coordinate_array.get((x, y)) > 0:
                    marked_points.append(x)

    bounds.append(min(marked_points))
    bounds.append(max(marked_points))

    return bounds


# From the given point, create a coordinate pair value
# and updates the array with the pair
def create_coordinates(data, width, height):
    # dict {(x,y) : alpha value}
    coordinate_arr = {}
    cur_width = 0
    cur_height = 0

    for point in data:
        if cur_height < height:
            if cur_width < width:
                coordinate_arr.update({(cur_width, cur_height): point})
                cur_width += 1
            else:
                cur_width = 0
                cur_height += 1
                coordinate_arr.update({(cur_width, cur_height): point})
                cur_width += 1
    return coordinate_arr



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
width, height = image.size
data = list(pixels.getdata(3))  # Only gets Alpha Channels
coord_arr = create_coordinates(data, width, height)
y_bounds = find_bounds(coord_arr, "Y", width, height)
x_bounds = find_bounds(coord_arr, "X", width, height)
