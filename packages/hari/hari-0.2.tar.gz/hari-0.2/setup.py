from setuptools import setup, find_packages
setup(
    name='hari',
    version='0.2',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'hari = hari:hello',
        ],
    },
)


