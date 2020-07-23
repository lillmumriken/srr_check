from setuptools import setup, find_packages

setup(
    name='srr_check',
    version='1.0',
    description='Compare a release on your filesystem to srrDB',
    entry_points = {
        'console_scripts': ['srr_check=srr_check.srr_check:main'],
    },
    packages=find_packages(),
    python_requires='>=3.6',
    install_requires=[
        "requests",
    ],
)
