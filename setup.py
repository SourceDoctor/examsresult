# coding=utf-8
from setuptools import setup, find_packages
package_templates = {"examsresult.lng." + package: ["*.lng", "1476313854_report_pencil.png"] for package in find_packages('examsresult/lng')}

setup(
    name='examsresult',
    packages=['examsresult', 'examsresult.models', 'examsresult.controls', 'examsresult.views'],
    package_data=package_templates,
    author='Thomas Berberich',
    author_email='thomasberb@googlemail.com',
    description='Database for Schoolclasses and their Exams',
    entry_points={
        'gui_scripts': [
            "examsresult = examsresult:run",
        ]
    },
    install_requires=['sqlalchemy', 'PyQt5', 'reportlab'],
    version='1.0',
)
