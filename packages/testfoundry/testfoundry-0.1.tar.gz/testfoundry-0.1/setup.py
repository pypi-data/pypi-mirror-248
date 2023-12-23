from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='testfoundry',
    version='0.1',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'testfoundry = testfoundry.__main__:main'
        ]
    },
    description='A Python test generator',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='Kyle Reynolds',
    author_email='kylereynoldsdev@gmail.com',
    url='https://github.com/KDreynolds/py_testgen',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
)