from setuptools import setup, find_packages

setup(
    name='print-0-world',
    version='0.1.0',
    author='Aman',
    author_email='aman.email@example.com',
    description='description of my package',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)