from setuptools import setup, find_packages


def read_version():
    with open('neets/neets.py', 'r') as file:
        for line in file:
            if line.startswith('NEETS_API_CLI_VERSION'):
                # Extract version and remove quotes
                return line.split('=')[1].strip().strip('\'"')


with open('requirements.txt') as f:
    dependencies = f.read().splitlines()

with open('README.md', 'r') as f:
    long_description = f.read()


entry_points = {
    'console_scripts': [
        'neets=neets.neets:cli',
    ],
}

setup(
    name='neets', 
    version=read_version(),
    description='CLI to interact with the neets.ai API',
    long_description=long_description,
    long_description_content_type='text/markdown', 
    author='NotJoeMartinez',
    url='https://github.com/NotJoeMartinez/neets-api-cli',  
    packages=find_packages(),
    install_requires=dependencies,
    entry_points=entry_points,
    python_requires='>=3.8',
)