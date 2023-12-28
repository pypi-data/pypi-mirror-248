from setuptools import setup

setup(
    name='test-gut',
    version='1.0.1',
    py_modules=['gut'],
    install_requires=['Click', ],
    entry_points={
        'console_scripts': [
            'test-gut = gut:cli'
        ]
    })
