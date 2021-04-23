# Description
This script takes images and uses transparent pixel grids in order to seperate each object into smaller files. A test image is included in order to see how this script works.

# Installation
To install:
```
pip install slicer
```

# Usage
```
cd {main folder}
slice {path to image file} {format}
```

# Examples
Uses test.png and outputs in default png format
```
slice test.png
```

To specify a different format, type the format like below
```
slice test.png jpg
```

This format works too
```
slice test.png .jpg
```


