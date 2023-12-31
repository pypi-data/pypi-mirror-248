import setuptools

long_description = ''
with open('README.md' , 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name="python_upsrtc",
    version="0.1.1",
    author="Mohd Sabahat",
    author_email="mohdsabahat123@gmail.com",
    description="An unofficial python wrapper for UPSRTC internal API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/mohdsabahat/python-upsrtc/tree/main",
    packages=setuptools.find_packages(),
    classifiers = [
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)