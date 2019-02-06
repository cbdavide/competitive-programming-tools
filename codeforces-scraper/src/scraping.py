
import re

from .util import Problem
from .util import TestCase

from bs4 import Tag
from bs4 import BeautifulSoup


INPUT_CSS_CLASS = '.input'
OUTPUT_CSS_CLASS = '.output'
PROBLEMS_CSS_CLASS = '.id'


class Scraper:

    def __init__(self, raw_html):
        self.html = BeautifulSoup(raw_html, 'html.parser')

    def scrap(self):
        raise Exception('Not Implemented')


class ProblemScraper(Scraper):

    def _clean_content(self, data):
        for line in data:
            if isinstance(line, Tag):
                if line.name == 'br':
                    yield '\n'
            else:
                yield line

    def _extract_content(self, selector):
        for element in self.html.select(selector):

            data = list(element.children)[1]
            cleaned_data = self._clean_content(data.contents)

            yield ''.join(cleaned_data).strip('\n')

    def scrap(self):
        inputs = self._extract_content(INPUT_CSS_CLASS)
        outputs = self._extract_content(OUTPUT_CSS_CLASS)

        return [TestCase(t[0], t[1]) for t in zip(inputs, outputs)]


class ContestScraper(Scraper):

    PATTERN = re.compile(r'[\\rn\s]')

    def _clean_content(self, data):
        clean = data.encode('unicode_escape')
        clean = clean.decode('utf-8')

        problem_id = self.PATTERN.subn('', clean)

        return problem_id[0]

    def _extract_content(self, selector):
        problems = self.html.select(selector)

        for problem in problems:

            children = list(problem.children)
            anchor_element = children[1]

            anchor_url = anchor_element['href']
            problem_id = self._clean_content(anchor_element.contents[0])

            yield problem_id, anchor_url

    def scrap(self):
        problems = self._extract_content(PROBLEMS_CSS_CLASS)

        return [Problem(x[0], x[1]) for x in problems]


class CodeforcesScraperFactory:

    @classmethod
    def contestScraper(cls):
        return ContestScraper

    @classmethod
    def problemScraper(cls):
        return ProblemScraper


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
