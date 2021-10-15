from setuptools import setup
import os

# Update on pypi:
#
# 1. delete old /dist
# 2. python3 -m pip install --upgrade build
# 3. python3 -m build
# 4. python3 -m twine upload dist/*
#


def read(filename):
    try:
        return open(os.path.join(os.path.dirname(__file__), filename)).read()
    except Exception as err:
        return ""


setup(name="customtkinter",
      version="1.3",
      author="Tom Schimansky",
      license="Creative Commons Zero v1.0 Universal",
      url="https://github.com/TomSchimansky/CustomTkinter",
      description="Create modern looking gui with tkinter and python",
      long_description_content_type="text/markdown",
      long_description=read('Readme_pypi.md'),
      packages=["customtkinter"],
      classifiers=["Operating System :: OS Independent",
                   "Programming Language :: Python :: 3",
                   "License :: CC0 1.0 Universal (CC0 1.0) Public Domain Dedication"],
      install_requires=["darkdetect"])
