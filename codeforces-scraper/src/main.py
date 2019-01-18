
from concurrent.futures import ThreadPoolExecutor

from src.os import create_folder
from src.os import save_problem_cases

from src.util import Problem
from src.request import get_html
from src.util import print_problem_list

from src.scraping import get_test_cases
from src.scraping import get_problem_list


CODEFORCES_BASE_URL = 'https://codeforces.com'


def download_cases(problem):

    def log():
        return "Downloading test cases of problem {1}/{0}".format(
            problem.id,
            problem.contest
        )

    test_cases_url = "{}{}".format(
        CODEFORCES_BASE_URL,
        problem.url
    )

    path = "{}/{}".format(problem.contest, problem.id)

    test_cases_html = get_html(test_cases_url)
    test_cases = list(get_test_cases(test_cases_html))

    print(log())
    for test_case in test_cases:
        problem.testCases.append(test_case)

    save_problem_cases(path, problem)


def create_contest(contest_id):

    contest_url = "{}/contest/{}".format(
        CODEFORCES_BASE_URL,
        contest_id
    )

    create_folder(contest_id)

    print("Getting the list of problems...")
    problem_list_html = get_html(contest_url)
    problem_list = list(get_problem_list(problem_list_html, contest_id))
    print_problem_list(problem_list)

    with ThreadPoolExecutor(max_workers=5) as executor:
        executor.map(download_cases, problem_list)


def create_problems(plain_problems):

    def to_problem_list():

        for plain in plain_problems:
            contest, id = plain.split('/')
            url = "/problemset/problem/{0}".format(
                plain,
                CODEFORCES_BASE_URL
            )

            yield Problem(id, url, contest)

    problems = list(to_problem_list())

    for p in problems:
        create_folder(p.contest)

    with ThreadPoolExecutor(max_workers=5) as executor:
        executor.map(download_cases, problems)
