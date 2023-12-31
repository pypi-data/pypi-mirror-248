# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['comic_ocr',
 'comic_ocr.dataset',
 'comic_ocr.dataset.annotated_manga',
 'comic_ocr.dataset.generated_manga',
 'comic_ocr.dataset.generated_single_line',
 'comic_ocr.models',
 'comic_ocr.models.localization',
 'comic_ocr.models.localization.conv_unet',
 'comic_ocr.models.recognition',
 'comic_ocr.models.recognition.crnn',
 'comic_ocr.models.recognition.fcn',
 'comic_ocr.models.recognition.trocr',
 'comic_ocr.types',
 'comic_ocr.utils']

package_data = \
{'': ['*']}

install_requires = \
['Pillow>=9.1,<10.0',
 'numpy>=1.21,<2.0',
 'opencv-python>=4.5.4.60,<5.0.0.0',
 'textdistance>=4.2.1,<5.0.0',
 'torch>=1.12.1,<2.0.0',
 'torchvision>=0.13.1,<0.14.0',
 'tqdm>=4,<5',
 'transformers>=4.23.1,<5.0.0']

setup_kwargs = {
    'name': 'comic-ocr',
    'version': '0.1.6',
    'description': 'An OCR library comic and manga',
    'long_description': None,
    'author': 'Wanasit T',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
