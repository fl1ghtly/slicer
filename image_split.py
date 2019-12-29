from PIL import Image
import os

left_arr = up_arr = right_arr = low_arr = []

def create_dir(dirName):
    if not os.path.exists(dirName):
        try:
            os.makedirs(dirName)
        except OSError:
            print('Error creating ' + dirName)

def crop(cut_arr, image):
    create_dir('./test')
    img_num = 1
    for cut in cut_arr:
        new_img = image.crop(cut)
        new_img.save('./test' + '/result' + img_num + '.png')
        img_num += 1

def create_tuple(left_arr, up_arr, right_arr, low_arr):
    cut_arr = list()
    if len(left_arr) == len(right_arr) == len(up_arr) == len(low_arr):
        for x in len(left_arr): 
            cut_tuple = tuple(left_arr[x], right_arr[x],
                              up_arr[x], low_arr[x])
            cut_arr.append
            if x >= len(left_arr):
                return cut_arr
    else:
        pass # TODO raise exception and print error

def store(left, upper, right, lower):
    if left is not None:
        left_arr.append(left)
    if upper is not None:
        up_arr.append(upper)
    if left is not None:
        right_arr.append(right)
    if left is not None:
        low_arr.append(lower)
    

def transparent(image, data): 
    width, height = image.size
    row_num = col_num = i = j = 0
    left = upper = right = lower = int()
    row_detect = col_detect = end_search = False 
    # Used incase there are more than 1 pix gap for upper bound

    # Possible problem: if statement only evaluates once and never again
    while col_num <= width - 1 and row_num <= height - 1: # does not reach, find out why
        #(left, *upper, right, *lower)      
            if i <= width - 1:
                if data[i + (width * row_num)] is not 0:
                    row_num += 1
                    #print("Row num is " + str(row_num))
                    i = 0
                    row_detect = True
                elif i == width - 1 and row_detect == False:
                    i = 0
                    upper += 1
                    row_num += 1
                    #print("Row num is " + str(row_num))
                elif i == width - 1 and row_detect == True:
                    lower = row_num
                    row_num += 1
                    #print("Row num is " + str(row_num))
                    row_detect = False
                    i = 0
                    store(None, upper, None, lower)
                    continue
                else:
                    i += 1

        #(*left, upper, *right, lower)
            if j <= height - 1:        
                if data[col_num + (j * width)] is not 0: 
                    col_num += 1
                    #print("Col num is " + str(col_num))
                    j = 0
                    col_detect = True
                elif j == height - 1 and col_detect == False:
                    j = 0
                    col_num += 1
                    #print("Col num is " + str(col_num))
                    left += 1
                elif j == height - 1 and col_detect == True:
                    right = col_num    
                    store(left, None, right, None)
                    col_detect = False
                    col_num += 1
                    #print("Col num is " + str(col_num))
                    j = 0
                    continue
                else:
                    j += 1
    else:
        print('reached') 
        arr = create_tuple(left_arr, up_arr, 
                           right_arr, low_arr)
        crop(arr, image)

image = Image.open('./test-images/test.png')
pixels = image.convert('RGBA')
data = list(pixels.getdata(3)) # Only gets Alpha Channels
transparent(image, data)
