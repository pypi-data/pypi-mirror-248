from setuptools import setup

setup(
    name='hinlang',
    version='0.1',
    py_modules=['Interpreter'],
    install_requires=[
        # List any dependencies here
    ],
    entry_points={
        'console_scripts': [
            'hinlang=Interpreter:main',
        ],
    },
)
