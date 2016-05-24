from setuptools import setup

setup(
    name="elv",
    packages=["elv"],
    version="1.0.12",
    description="Parser and query API for bank CSV account transactions",
    author="Christian Stigen Larsen",
    author_email="csl@csl.name",
    url="https://github.com/cslarsen/elv",
    download_url="https://github.com/cslarsen/elv/tarball/1.0.12",
    license="https://www.gnu.org/licenses/agpl-3.0.html",
    long_description=open("README.rst").read(),
    zip_safe=True,
    test_suite="tests",

    keywords=["bank", "csv", "transaction", "transactions", "money",
        "sparebank", "finance"],

    platforms=['unix', 'linux', 'osx', 'cygwin', 'win32'],

    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Console",
        "Natural Language :: English",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: POSIX",
        "Operating System :: Unix",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.1",
        "Programming Language :: Python :: 3.2",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: Implementation :: PyPy",
    ],
)
