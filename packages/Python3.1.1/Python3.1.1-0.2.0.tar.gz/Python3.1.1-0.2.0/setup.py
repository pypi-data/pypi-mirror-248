from setuptools import setup, find_packages

setup(
    name='Python3.1.1',
    version='0.2.0',
    packages=find_packages(),
    package_data={'tnsorflow': ['notebook/*.ipynb']},
    install_requires=[
        'nbformat',  # Add nbformat as a dependency
        # List your other dependencies here if any
    ],
    entry_points={
        'console_scripts': [
            'tnsorflow=tnsorflow.hello:hello',
        ],
    },
    author='Your Name',
    author_email='your.email@example.com',
    description='A simple package that prints "Hello from tnsorflow!"',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/yourusername/tnsorflow',
    license='MIT',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
)
