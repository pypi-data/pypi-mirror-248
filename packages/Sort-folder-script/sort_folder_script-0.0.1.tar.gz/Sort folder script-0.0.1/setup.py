from setuptools import setup, find_packages

setup(
    name='Sort folder script',
    version='0.0.1',
    author='Roman Kripak',
    url='https://github.com/romanlenger/homeworkTask7_Kripak',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'clean-folder = clean_folder.clean_folder.clean:main',
        ]
    }
)