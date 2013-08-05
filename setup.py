# -*- coding: utf-8 -*-
from setuptools import setup, find_packages


install_requires = (
    )
description = "An upgrade utility"


setup(
    name='cnx-upgrade',
    version='0.1',
    author='Connexions team',
    author_email='info@cnx.org',
    url="https://github.com/connexions/cnx-upgrade",
    license='LGPL, See aslo LICENSE.txt',
    description=description,
    packages=find_packages(),
    install_requires=install_requires,
    include_package_data=True,
    entry_points="""\
    [console_scripts]
    cnx-upgrade = cnxupgrade.cli:main
    """,
    # test_suite=''
    )