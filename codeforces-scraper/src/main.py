
from itertools import repeat
from concurrent.futures import ThreadPoolExecutor

from src.os import create_folder
from src.os import save_problem_cases

from src.util import Problem
from src.request import get_html

from src.scraping import get_test_cases
from src.scraping import get_problem_list


CODEFORCES_BASE_URL = 'https://codeforces.com'


def problem_log(*args, **kwargs):
    print(
        f'Downloading test cases for problem {args[0].contest}/{args[0].id}'
    )


def log(argfunc):

    def log_wrapper(func):

        def wrapper(*args, **kwargs):
            argfunc(*args, **kwargs)

            return func(*args, **kwargs)

        return wrapper
    return log_wrapper


@log(problem_log)
def download_cases(problem, kwargs):

    path = f"{problem.contest}/{problem.id}"
    test_cases_url = f"{CODEFORCES_BASE_URL}{problem.url}"

    test_cases_html = get_html(test_cases_url)
    test_cases = list(get_test_cases(test_cases_html))

    for test_case in test_cases:
        problem.testCases.append(test_case)

    save_problem_cases(path, problem, **kwargs)


def create_contest(contest_id, **kwargs):

    create_folder(contest_id, **kwargs)
    contest_url = f"{CODEFORCES_BASE_URL}/contest/{contest_id}"

    problem_list_html = get_html(contest_url)
    problem_list = get_problem_list(problem_list_html, contest_id)

    with ThreadPoolExecutor(max_workers=5) as executor:
        ex = executor.map(download_cases, problem_list, repeat(kwargs))
        # TODO: Handle possible errors


def create_problems(plain_problems, **kwargs):

    def to_problem_list():

        for plain in plain_problems:
            contest, id = plain.split('/')
            url = f"/problemset/problem/{plain}"
            yield Problem(id, url, contest)

    problems = list(to_problem_list())

    for p in problems:
        create_folder(p.contest, **kwargs)

    with ThreadPoolExecutor(max_workers=5) as executor:
        ex = executor.map(download_cases, problems, repeat(kwargs))
        # TODO: Handle possible errors
