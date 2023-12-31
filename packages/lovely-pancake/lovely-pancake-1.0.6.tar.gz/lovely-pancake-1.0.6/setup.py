from setuptools import setup

with open('README.md', encoding='utf-8') as f:
    long_description = f.read()


setup(

    name='lovely-pancake',
    version='1.0.6',
    author='Ahmet Duzduran',
    description='My lovely python package',
    packages=['lovelypancake'],
    long_description=long_description,
    long_description_content_type='text/markdown',
)
