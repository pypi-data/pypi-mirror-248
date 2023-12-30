#!/usr/bin/env python
"""
Install wagtail-charcount using setuptools
"""

with open("README.md", "r") as f:
    readme = f.read()

from setuptools import find_packages, setup

setup(
    name="wagtail-charcount",
    version="0.2.0",
    description="A wagtail character and word counting plugin for RichTextFields.",
    long_description=readme,
    long_description_content_type="text/markdown",
    author="Liam Brenner",
    author_email="liam@takeflight.com.au",
    url="https://github.com/takeflight/wagtail-charcount",
    install_requires=[
        "wagtail>=4.1",
    ],
    zip_safe=False,
    license="BSD License",
    packages=find_packages(),
    include_package_data=True,
    package_data={},
    classifiers=[
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Framework :: Django",
        "License :: OSI Approved :: BSD License",
    ],
)
