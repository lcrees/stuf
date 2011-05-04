'''setup stuf'''

from setuptools import setup

setup(
    name='stuf',
    version='0.1',
    description='''stuf has attributes''',
    long_description='''miscellaneous dot accessible dictionaries''',
    author='L. C. Rees',
    author_email='lcrees@gmail.com',
    license='BSD',
    packages = ['stuf'],
    test_suite='stuf.test',
    zip_safe = False,
    keywords='dict attributes collection mapping',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development',
        'Topic :: Software Development :: Libraries',
        'Topic :: Utilities',
    ],
)