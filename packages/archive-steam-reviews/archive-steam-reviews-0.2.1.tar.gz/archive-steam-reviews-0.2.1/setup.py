#!/usr/bin/env python
import re
from pathlib import Path

from setuptools import find_packages
from setuptools import setup


def read(*names, **kwargs):
    with Path(__file__).parent.joinpath(*names).open(encoding=kwargs.get("encoding", "utf8")) as fh:
        return fh.read()


setup(
    name="archive-steam-reviews",
    version="0.2.1",
    license="MIT",
    description="Scrape all Steam reviews from a specific profile",
    long_description="{}\n{}".format(
        re.compile("^.. start-badges.*^.. end-badges", re.M | re.S).sub("", read("README.rst")),
        re.sub(":[a-z]+:`~?(.*?)`", r"``\1``", read("CHANGELOG.rst")),
    ),
    author="Manuel Grabowski",
    author_email="git@manuelgrabowski.de",
    maintainer="Brie Carranza",
    maintainer_email="hi@brie.ninja",
    url="https://github.com/manuelgrabowski/archive-steam-reviews",
    packages=find_packages("src"),
    package_dir={"": "src"},
    py_modules=[path.stem for path in Path("src").glob("*.py")],
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        # complete classifier list: http://pypi.python.org/pypi?%3Aaction=list_classifiers
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Unix",
        "Operating System :: POSIX",
        "Operating System :: MacOS",
        "Operating System :: MacOS :: MacOS X",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
        "Topic :: Games/Entertainment",
        # uncomment if you test on these interpreters:
        # "Programming Language :: Python :: Implementation :: IronPython",
        # "Programming Language :: Python :: Implementation :: Jython",
        # "Programming Language :: Python :: Implementation :: Stackless",
        "Topic :: Utilities",
    ],
    project_urls={
        "Source Code": "https://github.com/manuelgrabowski/archive-steam-reviews",
        "Initial Release Post": "https://log.manuelgrabowski.de/post/archive-steam-reviews/",
        "Issue Tracker": "https://github.com/manuelgrabowski/archive-steam-reviews/issues",
    },
    keywords=[
        "steam","review","video game",
    ],
    python_requires=">=3.8",
    install_requires=[
        # eg: "aspectlib==1.1.1", "six>=1.7",
        "beautifulsoup4==4.12.2",
        "certifi==2023.7.22",
        "charset-normalizer==3.3.2",
        "idna==3.4",
        "markdownify==0.11.6",
        "python-dateutil==2.8.2",
        "requests==2.31.0",
        "six==1.16.0",
        "soupsieve==2.5",
        "urllib3==2.0.7",
    ],
    extras_require={
        # eg:
        #   "rst": ["docutils>=0.11"],
        #   ":python_version=="2.6"": ["argparse"],
    },
    entry_points={
        "console_scripts": [
            "archive-steam-reviews = archive_steam_reviews.cli:main",
        ]
    },
)
