from setuptools import find_packages, setup

setup(
    name='cystechpost',
    packages=find_packages(include=['errors', 'instagram', 'wordpress', 'system']),
    version='1.0.1',
    description='CYSTech POST: Python social media posting + publishing library.',
    author='Jordan C. McRae',
    install_requires=['requests'],
    setup_requires=['pytest-runner'],
    tests_require=['pytest'],
    test_suite='tests',
)