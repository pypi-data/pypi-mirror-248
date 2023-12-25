from setuptools import setup, find_packages
import toml 

# Get requirements from Pipfile
with open('Pipfile') as f:
    required = toml.load(f)['packages'].keys()
    
setup(
    name='Capella',
    version='2.3.5',
    packages=find_packages(),
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'capella = capella.__main__:main'
        ]
    },
    description='A Python package for celestial navigation',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Alex Spradling',
    author_email='alexspradling@gmail.com',
    url='https://github.com/AlexSpradling/Capella',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
    ],
    install_requires=required
)
