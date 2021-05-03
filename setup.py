"""
Created on 4 Sep 2020
Updated 23 Mar 2021

@author: Jade Page (jade.page@southcoastscience.com)

https://packaging.python.org/tutorials/packaging-projects/
https://packaging.python.org/guides/single-sourcing-package-version/
"""

import codecs
import os

from setuptools import setup, find_packages


# TODO: update scripts

# --------------------------------------------------------------------------------------------------------------------

def read(rel_path):
    here = os.path.abspath(os.path.dirname(__file__))
    with codecs.open(os.path.join(here, rel_path), 'r') as fp:
        return fp.read()


def get_version(rel_path):
    for line in read(rel_path).splitlines():
        if line.startswith('__version__'):
            return line.split("'")[1]
    else:
        raise RuntimeError("Unable to find version string.")


# --------------------------------------------------------------------------------------------------------------------

with open('requirements.txt') as req_txt:
    required = [line for line in req_txt.read().splitlines() if line]


setup(
    name='scs_mfr',
    version=get_version("scs_core/__init__.py"),
    description='High-level scripts and command-line applications for South Coast Science '
                'environmental monitor manufacturing, test and calibration.',
    author='South Coast Science',
    author_email='contact@southcoastscience.com',
    url='https://github.com/south-coast-science/scs_mfr',
    package_dir={'': 'src'},
    packages=find_packages('src'),
    classifiers=[
        'Development Status :: 4 - Beta',
        'Operating System :: POSIX',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    scripts=[
        'src/scs_mfr/afe_baseline.py',
        'src/scs_mfr/afe_calib.py',
        'src/scs_mfr/afe_conf.py',
        'src/scs_mfr/csv_reader.py',
        'src/scs_mfr/csv_writer.py',
        'src/scs_mfr/dfe_id.py',
        'src/scs_mfr/dfe_test.py',
        'src/scs_mfr/eeprom_read.py',
        'src/scs_mfr/eeprom_write.py',
        'src/scs_mfr/gps_conf.py',
        'src/scs_mfr/host_id.py',
        'src/scs_mfr/ndir_conf.py',
        'src/scs_mfr/opc_conf.py',
        'src/scs_mfr/osio_api_auth.py',
        'src/scs_mfr/osio_client_auth.py',
        'src/scs_mfr/osio_host_organisation.py',
        'src/scs_mfr/osio_project.py',
        'src/scs_mfr/psu_conf.py',
        'src/scs_mfr/pt1000_calib.py',
        'src/scs_mfr/dfe_conf.py',
        'src/scs_mfr/rtc.py',
        'src/scs_mfr/schedule.py',
        'src/scs_mfr/sht_conf.py',
        'src/scs_mfr/system_id.py',
        'src/scs_mfr/timezone.py',
    ],
    install_requires=required,
    platforms=['any'],
    python_requires=">=3.3",
)
