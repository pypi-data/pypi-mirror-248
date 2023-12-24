from setuptools import setup, find_packages

setup(
    name='staruxian',
    version='1.1.0',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'generate_pass = my_password_generator.generate:main',
        ],
    },
    description='Owned by: cosmoboy',
    author='Khurshed Ziyovaddinov',
    author_email='mrx555888@gmail.com',

)
