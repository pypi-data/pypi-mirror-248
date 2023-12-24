from setuptools import setup, find_packages

from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name="show_in_browser",
    version="0.1.6",
    author="Peter Rush; Mircea-Andrei Radu",
    url="https://github.com/pxr687/show_in_browser",
    description="A simple python package for rendering a Pandas DataFrames and matplotlib/plotly plots in a browser.",
    long_description=long_description,
    long_description_content_type='text/markdown',
    license="MIT",
    packages=find_packages("src"),
    package_dir={"": "src"},
    install_requires=[
    "pandas",
    "aspose-words"
    ],
 classifiers=[
    'Operating System :: POSIX :: Linux',
    'Operating System :: Microsoft :: Windows']
)