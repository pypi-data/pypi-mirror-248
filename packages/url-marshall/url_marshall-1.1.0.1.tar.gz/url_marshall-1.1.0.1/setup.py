from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='url_marshall',
    version='1.1.0.1',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/mdaseem03/url_marshall",
    packages=find_packages(),
    install_requires=[
        'argparse'
    ],
    entry_points={
        'console_scripts': [
            'url_marshall=url_marshall:main',
        ],
    },

)
