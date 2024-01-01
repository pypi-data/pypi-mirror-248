from setuptools import setup, find_packages
# Read requirements.txt
with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(
    name='kasa-carbon',
    version='0.1',
    packages=find_packages(),
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'kasa-carbon = kasa_carbon:main',
        ],
    },
    install_requires=requirements,
)