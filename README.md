# Description
Separates images that have transparent spaces in between objects into individual .png files that only contain those objects

# Installation
To install:
```
cd {main folder}
pip install -r requirements.txt
```
Main folder is the directory to image-split

# Usage
1. Open CMD in the Windows Start Menu
2. Input "cd 'image split directory'" where 'image split directory' is the path to the main image-split folder
3. Type "python image_split.py" with the arguments you want

# Examples
```
# Base format
python image_split.py {image file} {format}

# Uses test.png and outputs in default png format
python image_split.py test.png

# Use this format to specify a folder inside the main folder
python image_split.py ./test-images/test.png

# Use this format to specify a folder path instead
python image_split.py C:/Users/{user}/test-images/test.png

# To specify a different format, type the format like below
python image_split.py test.png jpg

# This format works too
python image_split.py test.png .jpg
```


