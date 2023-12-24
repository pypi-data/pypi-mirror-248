from setuptools import setup, find_packages

setup(
    name='regplates',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'pygame',
        'pygame_gui',
        'os',
        'tkinter',
        'itertools',
        'pygame.locals',
        'random',
        'pickle',
        'pandas'
    ],
    entry_points={
        'console_scripts': [
            'xxxxxxxxxx = main.py',
        ],
    },
)