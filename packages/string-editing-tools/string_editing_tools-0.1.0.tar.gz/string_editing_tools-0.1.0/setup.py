from setuptools import setup, find_packages

setup(
    name='string_editing_tools',  # Package name
    version='0.1.0',  # Version number
    author='Milan',
    author_email='magnatoshadow@gmail.com',
    description='A collection of utilities for editing and manipulating strings',
    packages=find_packages(),
    install_requires=[],  # List any dependencies here
    entry_points={
        'console_scripts': [
            'string_reverse=string_editing_tools.cli:reverse_string',  # Example command-line tool
        ]
    }
)
