# Description
This script takes images and uses transparent pixel grids in order to seperate each object into smaller files.

# Installation
To install:
```
cd {main folder}
pip install -r requirements.txt
```
Main folder is the directory to image-split

# Usage
```
cd {main folder}
python image_split.py {image file} {format}
```

# Examples
Uses test.png and outputs in default png format
```
python image_split.py test.png
```

Use this format to specify a folder inside the main folder
```
python image_split.py ./test-images/test.png
```

Use this format to specify a folder path instead
```
python image_split.py C:/Users/{user}/test-images/test.png
```

To specify a different format, type the format like below
```
python image_split.py test.png jpg
```

This format works too
```
python image_split.py test.png .jpg
```


