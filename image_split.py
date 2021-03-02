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


# Expands the current bounds of the search by 1 in 
# a direction (N, S, W, E)
# bound_current is a list of the top left coordinate
# and the bottom right coordinate of the current boundry
# bound_current is ordered [(xleft, yleft), (xright, yright)]
def expand(direction, bound_current):
    # Converts point tuples into lists in order to change
    bound_current = [list(point) for point in bound_current]
    if direction is "N":
        bound_current[0][1] -= 1
    elif direction is "S":
        bound_current[1][1] += 1
    elif direction is "W":
        bound_current[0][0] -= 1
    else:
        bound_current[1][0] += 1

    bound_current = [tuple(point) for point in bound_current]

    return bound_current

# Using the direction and new bounds
# Makes a lists of the newest included points
# of the new boundry
def find_difference(old_bound, new_bound, direction):
    point_list = []
    # New points must start at the boundry and 
    # not (0, 0)
    x = new_bound[0][0]
    y = new_bound[0][1]
    if direction is "N":
        while x < new_bound[1][0] + 1:
            point_list.append((x, new_bound[0][1]))
            x += 1
    elif direction is "S":
        while x < new_bound[1][0] + 1:
            point_list.append((x, new_bound[1][1]))
            x += 1
    elif direction is "W":
        while y < new_bound[1][1] + 1:
            point_list.append((new_bound[0][0], y))
            y += 1
    else:
        while y < new_bound[1][1] + 1:
            point_list.append((new_bound[1][0], y))
            y += 1

    return point_list


# Takes in a list of coordinates to check
# Returns False if the coord_list has any pixel 
# that has a non zero alpha value
# Returns True otherwise
def check_line(coord_list):
    for coord in coord_list:
        if coord_dic.get(coord) > 0:
            return False
        else:
            return True

# From the given point, create a coordinate pair value
# and updates the array with the pair
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
coord_dic = create_coordinates(data, width, height)
#start_search(coord_dic)
