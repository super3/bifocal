import os
from setuptools import setup


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name='bifocal',
    version='0.0.1',
    author='James Prestwich',
    author_email='james@storj.io',
    description=('Automated FIFO and LIFO accounting for cryptocurrencies.'),
    license='AGPLv3+',
    keywords='accounting bitcoin FIFO LIFO cryptocurrency',
    url='https://github.com/frdwrd/bifocal',
    packages=['bifocal'],
    long_description=read('README'),
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Topic :: Utilities',
        'License :: OSI Approved :: AGPL License',
    ],
)
