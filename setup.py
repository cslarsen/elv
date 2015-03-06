try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(
    name="elv",
    packages=["elv"],
    version="0.1.1",
    description="Parser and query API for bank account transactions",
    author="Christian Stigen Larsen",
    author_email="csl@csl.name",
    url="https://github.com/cslarsen/elv",
    download_url="https://github.com/cslarsen/elv/tarball/0.1.1",
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
    ],
)
