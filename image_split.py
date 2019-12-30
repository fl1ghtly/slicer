from PIL import Image
import os

left_arr, up_arr, right_arr, low_arr = [], [], [], []

def create_dir(dirName):
    if not os.path.exists(dirName):
        try:
            os.makedirs(dirName)
        except OSError:
            print('Error creating ' + dirName)

def crop(cut_arr, image):
    create_dir('./test')
    img_num = 1
    print(cut_arr)
    for cut in cut_arr:
        new_img = image.crop(cut)
        # TODO ask for user input in where to save and name
        new_img.save('./test' + '/result' + str(img_num) + '.png')
        img_num += 1

def create_tuple(left_arr, up_arr, right_arr, low_arr):
    cut_arr = []
    vertical = 0
    while vertical < len(up_arr):
        for x in range(len(left_arr)):
            cut_tuple = (left_arr[x], up_arr[vertical], 
                        right_arr[x], low_arr[vertical])
            cut_arr.append(cut_tuple)
        vertical += 1
    return cut_arr
        
def transparent(image, data): 
    width, height = image.size
    row_num = col_num = i = j = 0
    left = upper = right = lower = int()
    row_detect = col_detect = end_search = False 
    # Used incase there are more than 1 pix gap for upper bound

    while col_num <= width - 1 and row_num <= height - 1:
        #(left, *upper, right, *lower)      
            if i <= width - 1:
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

        #(*left, upper, *right, lower)
            if j <= height - 1:        
                if data[col_num + (j * width)] is not 0: 
                    col_num += 1
                    j = 0
                    col_detect = True
                elif j == height - 1 and col_detect == False:
                    j = 0
                    col_num += 1
                    left += 1
                elif j == height - 1 and col_detect == True:
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
        crop(arr, image)

# TODO ask for user input for image
image = Image.open('./test-images/test.png')
pixels = image.convert('RGBA')
data = list(pixels.getdata(3)) # Only gets Alpha Channels
transparent(image, data)
