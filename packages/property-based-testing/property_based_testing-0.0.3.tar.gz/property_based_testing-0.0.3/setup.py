import pathlib

from setuptools import find_packages, setup

import property_based_testing

here = pathlib.Path(__file__).parent

packages = find_packages(exclude=('tests',))

setup(
    name='property_based_testing',
    version=property_based_testing.__version__,
    description='property testing',
    long_description='',
    long_description_content_type='text/markdown',
    url='https://github.com/wpbindt/property_based_testing',
    author='Wessel Bindt',
    author_email='wesselbindt@gmail.com',
    license='GNU',
    classifiers=[
        'License :: OSI Approved '
        ':: GNU General Public License v3 or later (GPLv3+)',
        'Programming Language :: Python :: 3.11'
    ],
    packages=packages,
    include_package_data=True,
)
