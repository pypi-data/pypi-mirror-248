#!/usr/bin/python

import os
from setuptools import setup, find_packages
from dataviewer.dataviewer import APPLICATION_VERSION

MODULE_NAME      = 'dataframeviewer'
FOLDER_NAME      = MODULE_NAME
VERSION          = APPLICATION_VERSION
DESCRIPTION      = 'PyQt5 application to visualize pandas DataFrames'
LONG_DESCRIPTION = 'PyQt5 GUI application to show DataFrame in QTableViews and generate plots'

# Setting up
setup(
        # The name must match the folder name in the same directory
        name=MODULE_NAME, 
        folder=FOLDER_NAME,
        version=VERSION,
        author="Rafael Arvelo",
        author_email="rafaelarvelo1@gmail.com",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        packages=find_packages() +
                 [os.path.join(FOLDER_NAME, p) for p in find_packages(where=FOLDER_NAME)],
        install_requires=['pandas', 'numpy', 'PyQt5', 'openpyxl', 'matplotlib'],
        entry_points={'console_scripts' : ['dataviewer=dataviewer.dataviewer:main']},
        python_requires='>=3.6',
        classifiers= [
            "Programming Language :: Python :: 3",
            "Operating System :: MacOS :: MacOS X",
            "Operating System :: Microsoft :: Windows",
        ]
)
