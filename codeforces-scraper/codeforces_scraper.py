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

VALIDATORS = dict()


def register(func):
    VALIDATORS[func.__name__] = func
    return func


def validate(func):
    def wrapper(*args, **kwargs):

        for k, v in VALIDATORS.items():
            v(*args)

        return func(*args, **kwargs)
    return wrapper


@register
def validate_output_path(arguments):
    if arguments['--output'] and not exists(arguments['--output']):
        raise Exception('Output path does not exist...')


@register
def validate_template_path(arguments):
    if arguments['--template'] and not exists(arguments['--template']):
        raise Exception('Template file does not exist...')


@validate
def cli(arguments):
    options = {}

    if arguments['--output']:
        options['base_path'] = arguments['--output']

    if arguments['--template']:
        options['template_path'] = arguments['--template']

    if arguments['contest'] and arguments['<contest_id>']:
        create_contest(arguments['<contest_id>'], **options)
        sys.exit(0)

    if arguments['problem'] and arguments['<problem_id>']:
        create_problems(arguments['<problem_id>'], **options)
        sys.exit(0)


if __name__ == '__main__':
    arguments = docopt(__doc__)
    cli(arguments)
