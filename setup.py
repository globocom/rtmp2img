from os.path import dirname, abspath, join
from setuptools import setup

with open(abspath(join(dirname(__file__), 'README.md'))) as fileobj:
    README = fileobj.read().strip()

setup(
    name='rtmp2img',
    description='Save images from rtmp live videos',
    long_description=README,
    author='Globo.com',
    url='https://github.com/globocom/rtmp2img',
    version='0.1.5',
    zip_safe=False,
    include_package_data=True,
    entry_points={
        'console_scripts':
        ['rtmp2img = rtmp2img.cli:main'],
        },
    packages=[
        'rtmp2img',
        ],
    install_requires=[
        'requests==1.1.0',
		'sh==1.07',
		'wsgiref==0.1.2',
        ],
)
