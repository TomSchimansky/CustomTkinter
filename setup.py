from setuptools import setup
import os

# Update on pypi:
#
# 1. delete old /dist
# 2  increase both version numbers
# 3. python -m pip install --upgrade build
# 4. python -m build
# 5. python -m twine upload dist/*
#


setup(name="customtkinter",
      version="3.11",
      author="Tom Schimansky",
      license="Creative Commons Zero v1.0 Universal",
      url="https://github.com/TomSchimansky/CustomTkinter",
      description="Create modern looking gui with tkinter and python",
      long_description_content_type="text/markdown",
      long_description="# CustomTkinter UI-Library\n\nDetailed Information: https://github.com/TomSchimansky/CustomTkinter",
      include_package_data=True,
      packages=["customtkinter", "customtkinter.widgets"],
      classifiers=["Operating System :: OS Independent",
                   "Programming Language :: Python :: 3",
                   "License :: CC0 1.0 Universal (CC0 1.0) Public Domain Dedication"],
      install_requires=["darkdetect"])
