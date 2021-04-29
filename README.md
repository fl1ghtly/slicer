![GitHub release (latest by date)](https://img.shields.io/github/v/release/fl1ghtly/slicer?style=flat-square)
![PyPI - Downloads](https://img.shields.io/pypi/dm/slicer-img?style=flat-square)
![GitHub](https://img.shields.io/github/license/fl1ghtly/slicer?style=flat-square)
# Description
This script takes images and uses transparent pixel grids in order to seperate each object into smaller files. A test image is included in order to see how this script works.

# Requirements
This package needs Pillow which can be done through:
```
pip install Pillow
```

# Installation
To install:
```
pip install slicer-img
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


