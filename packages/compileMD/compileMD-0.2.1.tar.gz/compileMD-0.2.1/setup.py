from setuptools import setup, find_packages

# read the contents of your README file
from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "../README.md").read_text()

setup (
    name="compileMD",
    version='0.2.1',
    description='Compiles multiple markdown files into a single README.md',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author="Ashish S. Maharjan",
    author_email="<hello@amaharjan.de>",
    url='https://github.com/asis2016/compileMD',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'compileMD = compileMD.compile_markdown:compile_markdown',
        ],
    },
    keywords=['python', 'markdown'],
    license='MIT',
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
    ]
)
