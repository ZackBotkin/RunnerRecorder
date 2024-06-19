from setuptools import setup, find_packages

setup(
    name='runner',
    version='0.1',
    packages=find_packages(include=['runner', 'runner.*']),
    install_requires=[
        # Add any dependencies required by your package
        'pandas',
        'matplotlib',
        'numpy',
        'tk',
    ],
    entry_points={
        'console_scripts': [
            'runnerreader=runner.src.main:main',
        ],
    },
)

