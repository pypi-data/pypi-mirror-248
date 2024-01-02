from setuptools import setup, find_packages


with open('README.md') as _f:
    desc: str = _f.read()

setup(
    name='tooltils',
    description='A lightweight python utility package built on the standard library',
    long_description=desc,
    python_requires='>=3.7',
    license='MIT License',
    author='feetbots',
    author_email='pheetbots@gmail.com',
    packages=find_packages(exclude=['*tests*', '*.tests', '*.tests.*', 'tests.*', 'tests']),
    ext_modules=[],
    requires=[],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.12",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ],
    test_suite='tests'
)
