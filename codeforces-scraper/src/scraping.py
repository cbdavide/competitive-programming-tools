
import re

from .util import Problem
from .util import TestCase

from bs4 import Tag
from bs4 import BeautifulSoup


INPUT_CSS_CLASS = '.input'
OUTPUT_CSS_CLASS = '.output'
PROBLEMS_CSS_CLASS = '.id'


def get_test_cases(raw_html):

    def clean(elements):
        for element in elements:
            if isinstance(element, Tag):
                if element.name == 'br':
                    yield '\n'
            else:
                yield element

    def extract(html, selector):

        for tag in html.select(selector):
            data = list(tag.children)[1].contents
            data = clean(data)
            yield ''.join(data).strip('\n')

    html = BeautifulSoup(raw_html, 'html.parser')

    input = list(extract(html, INPUT_CSS_CLASS))
    output = list(extract(html, OUTPUT_CSS_CLASS))

    for x in zip(input, output):
        yield TestCase(x[0], x[1])


def get_problem_list(raw_html, contest_id):

    pattern = re.compile(r'[\\rn\s]')

    def clean(string):
        clean = string.encode('unicode_escape')
        clean = clean.decode('utf-8')

        problem_id = pattern.subn('', clean)

        return problem_id[0]

    def extract(problem):
        anchor = list(problem.children)[1]
        return anchor['href'], clean(anchor.contents[0])

    html = BeautifulSoup(raw_html, 'html.parser')

    problems_table = html.select(PROBLEMS_CSS_CLASS)

    for problem in problems_table:
        url, id = extract(problem)
        yield Problem(id, url, contest_id)


if __name__ == '__main__':

    from request import get_html

    url = 'https://codeforces.com/contest/1091/problem/G'
    raw_html = get_html(url)

    problems = get_test_cases(raw_html)

    for problem in problems:
        print(problem)

    # url = 'https://codeforces.com/contest/1100'
    # raw_html = get_html(url)
    # problems = get_problem_list(raw_html)
    # for problem in problems:
    #     print(problem)
