from setuptools import setup, find_packages

setup (
    name="compileMD",
    version='0.2.0',
    description='Compiles multiple markdown files into a single README.md',
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
