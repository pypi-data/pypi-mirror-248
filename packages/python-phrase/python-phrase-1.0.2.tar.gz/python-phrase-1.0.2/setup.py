from setuptools import setup

setup(
    name='python-phrase',
    version='1.0.2',
    description='First release for this Seven Technologies Clouds API, the PythonRestCLI',
    py_modules=['app'],
    install_requires=['Click'],
    entry_points={
        'console_scripts': [
            'python-phrase=app:cli',
        ],
    },
)
