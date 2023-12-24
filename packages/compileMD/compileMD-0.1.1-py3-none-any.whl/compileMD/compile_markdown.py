#!/usr/bin/env python3

__author__ = 'Ashish Singh Maharjan'

import os

MD_LOC = './md_docs'
README = './README.md'


def compile_markdown():
    '''
    Compiles a collection of markdown file into single README.md.
    '''
    files = sorted(os.listdir(MD_LOC))

    with open(README, 'w') as output_file:

        for file in files:
            with open(os.path.join(MD_LOC, file)) as input_file:
                print(f'[info] Compiling {file} into {README}')
                content = input_file.read() + '\n'
                output_file.write(content)


if __name__ == '__main__':
    compile_markdown()