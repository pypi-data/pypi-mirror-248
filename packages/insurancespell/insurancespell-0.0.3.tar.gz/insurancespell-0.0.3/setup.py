# -*- coding: utf-8 -*-
from setuptools import setup
from setuptools import find_packages
requirements = [
    'pythainlp>=3.10',
    'sklearn-crfsuite'
]
with open("README.md", "r", encoding="utf-8") as f:
    readme = f.read()

setup(
    name='insurancespell',
    version = '0.0.3',
    description="Thai insurance Spell Check",
    author='Thiraphat Chorakhe',
    author_email='thiraboaty@gmail.com',
    long_description=readme,
    long_description_content_type="text/markdown",
    url='https://github.com/Thiraphat-DEV/Insurance-Spell',
    packages=find_packages(),
    package_data={'insurancespellcheck': ['sp.model']},
    include_package_data=True,
    install_requires=requirements,
    license='Apache Software License 2.0',
    zip_safe=False,
    keywords='insurance',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: Implementation'],
)
