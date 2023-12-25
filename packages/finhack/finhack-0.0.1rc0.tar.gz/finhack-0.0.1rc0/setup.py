from setuptools import setup, find_packages
setup(
    name='finhack',
    version='0.0.1c',
    author='woldy',
    description='A scalable quantitative financial analysis framework.',
    packages=find_packages(),
    package_data={
        'finhack': ['finhack/*']
    },
)
