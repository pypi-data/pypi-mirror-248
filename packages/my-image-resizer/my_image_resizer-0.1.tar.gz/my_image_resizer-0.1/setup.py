from setuptools import setup, find_packages

setup(
    name='my_image_resizer',
    version='0.1',
    packages=find_packages(),
    #check pill is installed
    install_requires=[
        'Pillow',  
    ],
    author='Jolomi',
    description='Image resizing package',
    keywords='image resize PIL',
)
