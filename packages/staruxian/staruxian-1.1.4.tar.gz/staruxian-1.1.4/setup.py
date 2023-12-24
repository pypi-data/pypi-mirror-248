from setuptools import setup, find_packages

setup(
    name='staruxian',
    version='1.1.4',
    packages=find_packages(),
    author='Khurshed Ziyovaddinov',
    author_email='mrx555888@gmail.com',
    description='Hello I am cosmoboy',
    install_requires=[
    ],
    entry_points={
        "console_scripts": [
            "staruxian = staruxian:hello"
        ],
    },
)
