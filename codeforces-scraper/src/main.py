
import threading
from concurrent.futures import ThreadPoolExecutor

from src.os import create_folder
from src.os import save_problem_cases

from src.request import get_html

from src.scraping import get_test_cases
from src.scraping import get_problem_list


CODEFORCES_BASE_URL = 'https://codeforces.com'


def download_cases(problem):
    test_cases_url = "{}{}".format(
        CODEFORCES_BASE_URL,
        problem.url
    )

    path = "{}/{}".format(problem.contest, problem.id)

    test_cases_html = get_html(test_cases_url)
    test_cases = get_test_cases(test_cases_html)

    for test_case in test_cases:
        problem.testCases.append(test_case)

    save_problem_cases(path, problem)


def create_contest(contest_id):

    contest_url = "{}/contest/{}".format(
        CODEFORCES_BASE_URL,
        contest_id
    )

    create_folder(contest_id)

    problem_list_html = get_html(contest_url)
    problem_list = get_problem_list(problem_list_html, contest_id)

    with ThreadPoolExecutor(max_workers=5) as executor:
        executor.map(download_cases, problem_list)
