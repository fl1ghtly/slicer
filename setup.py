import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open('requirements.txt') as f:
    requirements = f.readlines()
	
setuptools.setup(
    name="slicer-img",
    version="2.1.1",
    author="James Nguyen",
    description="Slices an image into its constituent parts",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/fl1ghtly/slicer",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
	install_requires = requirements,
	entry_points = {
		'console_scripts': [
			'slice = slice.image_split:start_slice'
		]
	}
)
