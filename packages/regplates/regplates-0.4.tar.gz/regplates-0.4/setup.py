from setuptools import setup, find_packages

setup(
    name='regplates',
    version='0.4',
    packages=find_packages(),
    install_requires=[
        'pygame',
        'pygame_gui',
        'tkinter',
        'itertools',
        'pickle',
        'pandas'
    ],
    entry_points={
        'console_scripts': [
            'xxxxxxxxxx = Python.main:main_function',
        ],
    },
)