from setuptools import setup, find_packages

setup(
    name='aadhaar-detection',
    version='0.8',
    packages=find_packages(),
    install_requires=[
        'numpy',
        'opencv-python',
        'tensorflow>=2.7'
    ],
    author='Girinath',
    author_email='girinathr@simplfin.tech',
    description='Aadhaar card detection library',
    long_description='A library for detecting Aadhaar cards in images.',
    url='https://gitlab.com/ntechgrp/simpldocz_backend/-/tree/main/Aadhaar_Detection',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
)


