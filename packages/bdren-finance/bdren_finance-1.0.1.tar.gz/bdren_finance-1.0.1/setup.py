from setuptools import setup, find_packages

setup(
    name='bdren_finance',
    version='1.0.1',
    author='Shuvo',
    author_email='shuvo.punam@gmail.com',
    description='BdREN Finance',
    packages=find_packages(
        include=[
            'bdren_finance',
            'bdren_finance.*',
        ]
    ),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
