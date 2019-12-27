from PIL import Image
import os

def create_dir(dirName):
    if not os.path.exists(dirName):
        try:
            os.makedirs(dirName)
        except OSError:
            print('Error creating ' + dirName)

def crop(cut_arr, image):
    create_dir('./test')
    for cut in cut_arr:
        new_img = image.crop(cut)
        new_img.save('./test' + '/result' + cut + '.png')

def transparent(image, data):
    # TODO define image class with these variables
    width, height = image.size
    row_num = 0
    col_num = 0
    row_detect = False # Used incase there are more than 1 pix gap for upper bound
    col_detect = False
    vertical = 0, 0
    horizontal = 0, 0
    left = 0
    upper = 0
    right = 0
    lower = 0
    i = 0
    j = 0
    cut_arr = []

    #(left, *upper, right, *lower)
    while i <= width - 1:
        if row_num <= height - 1:
            if data[i + (width * row_num)] is not 0:
                row_num += 1
                i = 0
                row_detect = True
            elif i == width - 1 and row_detect == False:
                i = 0
                upper += 1
                row_num += 1
            elif i == width - 1 and row_detect == True:
                lower = row_num
                vertical = upper, lower
                break
                # store the values then 
                # reset to continue
                # will not work after first line
            else:
                i += 1

    #(*left, upper, *right, lower)
    while j <= height - 1: 
        if col_num <= width - 1:
            if data[col_num + (j * width)] is not 0: 
                print(col_num + (j * width))
                col_num += 1
                j = 0
                col_detect = True
            elif j == height - 1 and col_detect == False:
                j = 0
                col_num += 1
                left += 1
            elif j == height - 1 and col_detect == True:
                right = col_num    
                horizontal = left, right
                break
            else:
                j += 1          

    if right or lower is not 0:
        # TODO: Create an array that stores the cuts
        # does not store all values
        cut = horizontal[0], vertical[0], horizontal[1], vertical[1]
        cut_arr.append(cut)
        print(cut_arr)
        # activate function when there is no more new values
        #crop(cut_arr, image)

image = Image.open('test.png')
pixels = image.convert('RGBA')
data = list(pixels.getdata(3)) # Only gets Alpha Channels
transparent(image, data)
