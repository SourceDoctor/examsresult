# coding=utf-8
from setuptools import setup, find_packages
package_templates = {"examsresult.lng." + package: ["*.lng"] for package in find_packages('examsresult/lng')}

setup(
    name='examsresult',
    packages=['examsresult'],
    package_data=package_templates,
    author='Thomas Berberich',
    author_email='thomasberb@googlemail.com',
    description='Database for Schoolclasses and their Exams',
    entry_points={
        'gui_scripts': [
            "examsresult = examsresult:run",
        ]
    },
    install_requires=['sqlalchemy'],
    version='1.0',
)
