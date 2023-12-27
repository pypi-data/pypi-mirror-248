from setuptools import setup

setup(
    name='test-gut',
    version='1.0.0',
    py_modules=['gut'],
    install_requires=['Click', ],
    entry_points={
        'console_scripts': [
            'gut = gut:cli'
        ]
    })
