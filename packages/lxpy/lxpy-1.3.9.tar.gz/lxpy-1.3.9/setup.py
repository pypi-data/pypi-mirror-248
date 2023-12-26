#-*- coding:utf-8 -*-
# @Author  : lx

from setuptools import setup, find_packages

with open("README.rst", "r") as f:
  long_description = f.read()

setup(
    name = 'lxpy',
    url='https://github.com/lixi5338619/lxpy.git',
    version = '1.3.9',
    description='Web crawler and data processing toolkit !',
    long_description=long_description,
    #packages = find_packages(),
    packages = ['lxpy','lxpy/encrypt'],
    author = 'ying5338619',
    author_email = '125066648@qq.com',
    platforms = ["all"],
    install_requires=["wheel"],
    )



# python setup.py sdist bdist_wheel
# twine upload dist/*

