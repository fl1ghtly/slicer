# Description
This script takes images and uses transparent pixel grids in order to seperate each object into smaller files. A test image is included in order to see how this script works.

# Installation
To install:
```
cd {main folder}
pip install -r requirements.txt
```
Main folder is the directory to slicer

# Usage
```
cd {main folder}
python {path to image_split.py} {image file} {format}
```

# Examples
Uses test.png and outputs in default png format
```
python ./slice_img/image_split.py ./test-images/test1.png
```

To specify a different format, type the format like below
```
python ./slice_img/image_split.py ./test-images/test1.png jpg
```

This format works too
```
python ./slice_img/image_split.py ./test-images/test1.png .jpg
```


