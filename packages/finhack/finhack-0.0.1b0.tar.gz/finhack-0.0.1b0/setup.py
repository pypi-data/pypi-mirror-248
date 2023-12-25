from setuptools import setup

setup(
    name='finhack',
    version='0.0.1b',
    author='woldy',
    description='A scalable quantitative financial analysis framework.',
    packages=['finhack'],
    package_data={
        'finhack': ['finhack/*']
    },
)
