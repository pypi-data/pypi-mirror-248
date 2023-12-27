#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
THIS FILE IS PART OF NETWORK FOR MWAFU LIBRARY LOVE BOOK STORE BY MATT BELFAST BROWN
setup.py - The core part of the Foreign Name Translator.

Author: Matt Belfast Brown
E-mail: thedayofthedo@gmail.com
Creat Date: 2023-12-25
Version Date: 2023-12-26
Version: 0.0.1

THIS PROGRAM IS FREE FOR EVERYONE,IS LICENSED UNDER GPL-3.0
YOU SHOULD HAVE RECEIVED A COPY OF GPL-3.0 LICENSE.

Copyright (C) 2023 Matt Belfast Brown

This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as
published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty
of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.
You should have received a copy of the GNU General Public License along with this program.  If not,
see <http://www.gnu.org/licenses/>.
"""

from setuptools import find_packages, setup

with open("Descriptiption.md", "r", encoding="utf-8") as dest_pimd:
    long_description = dest_pimd.read()

setup(
        name="ForeNameTranslator",
        version="0.0.1",

        author="Matt Belfast Brown",
        author_email="thedayofthedo@gmail.com",
        license="GPL-3.0 LICENSE",

        description="Tool lib of network for Love Book Store Volunteer Association of NWAFU by Matt Belfast Brown",
        long_description=long_description,
        long_description_content_type="text/markdown",
        keywords=["pip", "name", "translator"],

        url="https://github.com/thedayofthedoctor/fnt",
        project_urls={
            "Documentation": "http://belfast.web3v.work/program/doc/fnt/",
            "Bug Tracker": "https://github.com/thedayofthedoctor/fnt/issues",
            },

        packages=find_packages(),
        py_modules=["ForeNameTranslator.__init__", "ForeNameTranslator.mode.__init__",
                    "ForeNameTranslator.mode.mode_FNM_Tra", "ForeNameTranslator.mode.mode_TRA_Api"],
        include_package_data=True,
        zip_safe=True,

        classifiers=[
            "Programming Language :: Python :: 3.7",
            "Programming Language :: Python :: 3.8",
            "Programming Language :: Python :: 3.9",
            "Programming Language :: Python :: 3.10",
            "Programming Language :: Python :: 3.11",
            "Programming Language :: Python :: 3.12",
            "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
            ],
        platforms="any",
        install_requires=["requests"],
        python_requires=">=3.7,<=3.12"
        )
