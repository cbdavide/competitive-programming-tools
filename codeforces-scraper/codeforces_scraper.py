"""
Codeforces scraper

This CLI downloads the test cases of codeforces problems.

It has two modes of use, it can be used to download a determined set of
problems or it can download all the problems of a contest.

Usage:
    codeforces_scraper contest <contest_id> [--output=<dir>] [--template=<templ>]
    codeforces_scraper problem <problem_id>... [--output=<dir>] [--template=<templ>]
    codeforces_scraper (-h | --help)

Example:
    codeforces_scraper contest 1097
    codeforces_scraper problem 1036/C 1081/C
    codeforces_scraper contest 1097 --template=tpl.cpp
    codeforces_scraper contest 1097 --output=/home/user/competitive-programming
"""

import sys
from docopt import docopt
from src.os import exists
from src.main import create_contest
from src.main import create_problems


def cli(arguments):

    def validate():
        '''
            This function raises an exception in case that the arguments
            are not consistent.
        '''

        if arguments['--output'] and not exists(arguments['--output']):
            raise Exception('Output path does not exist...')

        if arguments['--template'] and not exists(arguments['--template']):
            raise Exception('Template file does not exist...')

    validate()

    options = {}
    if arguments['--output']:
        options['base_path'] = arguments['--output']

    if arguments['contest'] and arguments['<contest_id>']:
        create_contest(arguments['<contest_id>'], **options)
        sys.exit(0)

    if arguments['problem'] and arguments['<problem_id>']:
        create_problems(arguments['<problem_id>'], **options)
        sys.exit(0)


if __name__ == '__main__':
    arguments = docopt(__doc__)
    cli(arguments)
