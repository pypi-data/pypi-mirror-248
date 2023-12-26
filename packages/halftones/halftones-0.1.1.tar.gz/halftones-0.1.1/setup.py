from setuptools import setup, find_packages

# Read the contents of your README file
with open('README.md', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='halftones',
    version='0.1.1',
    packages=find_packages(),
    description='Python package for processing and creating halftone images',
    author='Erkin Ötleş',
    author_email='hi@eotles.com',
    url='https://github.com/eotles/halftones_pkg',
    long_description=long_description,
    long_description_content_type='text/markdown',
    install_requires=[
        'opencv-python',
        'matplotlib',
        'numpy',
        'Pillow',  # PIL is included in Pillow
    ],
)
