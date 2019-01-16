"""
Codeforces scraper

This CLI downloads the test cases of codeforces problems.

It has two modes of use, it can be used to download a determined set of
problems or it can download all the problems of a contest.

Usage:
    codeforces_scraper contest <contest_id>
    codeforces_scraper problem <problem_id>...
    codeforces_scraper (-h | --help)

Example:
    codeforces_scraper contest 1097
    codeforces_scraper problem 1036/C 1081/C

"""

import sys
from docopt import docopt
from src.main import create_contest
from src.main import create_problems


def cli():
    arguments = docopt(__doc__)

    if arguments['contest'] and arguments['<contest_id>']:
        create_contest(arguments['<contest_id>'])
        sys.exit(0)

    if arguments['problem'] and arguments['<problem_id>']:
        create_problems(arguments['<problem_id>'])
        sys.exit(0)


if __name__ == '__main__':
    cli()
