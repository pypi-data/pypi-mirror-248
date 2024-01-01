from setuptools import find_packages, setup
setup(
    name='statshub',
    packages=find_packages(),
    version='0.0.5',
    description='Python Library to perform various Mathematical and Statical Operations.',
    author='Savi',
    license='MIT',
    install_requires=[],
    setup_requires=['pytest-runner', 'wheel'],
    tests_require=['pytest==4.4.1'],
    test_suite='tests',
)