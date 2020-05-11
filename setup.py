# coding = utf-8

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

# 这是一个字典
config = {
    'description': 'My Project',
    'author': 'My name',
    'url': 'URL to get it at',
    'download_url': 'Where to download it.',
    'author_email': 'My email.',
    'version': '0.1',
    'install_requires': ['nose'],
    'packages': ['NAME'],
    'scripts': [],
    'name': 'project_name'
}

setup(**config)
