from setuptools import setup, find_packages

setup(
    name='matplotilib',
    version='0.4.1',
    packages=find_packages(),
    package_data={'matplotilib': ['notebook/*.ipynb']},
    install_requires=[
        'nbformat','IPython'  # Add nbformat as a dependency
        # List your other dependencies here if any
    ],
    entry_points={
        'console_scripts': [
            'matplotilib=matplotilib.hello:hello',
        ],
    },
    description='',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
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
