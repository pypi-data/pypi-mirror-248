from setuptools import setup, find_packages
# Read requirements.txt
with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(
    name='kasa-carbon',
    packages=find_packages(),
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'kasa-carbon = kasa_carbon:main_wrapper',
        ],
    },
    install_requires=requirements,
)