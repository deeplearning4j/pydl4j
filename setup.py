from setuptools import setup
from setuptools import find_packages

setup(
    name='pydl4j',
    version='0.1.1',
    packages=find_packages(),
    install_requires=['jnius'],
    include_package_data=True,
    license='MIT',
    description='Java dependency management for Python projects using DL4J',
    url='https://github.com/deeplearning4j/pydl4j',
    entry_points={
        'console_scripts': [
            'pydl4j=pydl4j.cli:handle'
        ]
    },
    classifiers=[
        'Environment :: Console',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3'
    ]
)
