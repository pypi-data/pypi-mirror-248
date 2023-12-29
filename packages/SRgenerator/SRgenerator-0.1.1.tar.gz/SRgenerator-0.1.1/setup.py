from setuptools import setup, find_packages

classifiers = [
    'Development Status :: 4 - Beta',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: BSD License',
    'Operating System :: MacOS',
    'Operating System :: POSIX',
    'Operating System :: Unix',
    'Operating System :: Microsoft',
    'Operating System :: OS Independent',
    'Programming Language :: Python :: 3',
]

with open("README.txt", "r") as fh:
    long_description = fh.read()

setup(
    name                = 'SRgenerator',
    version             = '0.1.1',
    description         = "Stereo operation for chemicals based on RDkit package",
    long_description    = long_description,
    author              = 'Mola Lin',
    author_email        = 'acps91012@gmail.com',
    license             = 'BSD',
    packages            = find_packages(),
    install_requires    = ['selfies >= 2.0.0', 'rdkit >= 2023.3.1'],
    classifiers         = classifiers,
    package_data={
        '':['*.csv'],
        'bandwidth_reporter':['*.csv']
               },
    python_requires='>=3.6',
)
