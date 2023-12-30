from setuptools import setup, find_packages

setup(
    name='meta_translate',
    version='0.0.1',
    author='TAWSIF AHMED',
    author_email='sleeping4cat@outlook.com',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    packages=find_packages(),
    install_requires=[
        'transformers',
        'sentencepiece',
        'torch',
    ],
)
