import os
from itertools import repeat
from concurrent.futures import ThreadPoolExecutor


INPUT_SUFFIX = 'input'
OUTPUT_SUFFIX = 'output'
FILE_NAME_FORMAT = "{}_{}.{}"


def exists(path):
    return os.path.exists(path)


def create_folder(path, **kwargs):
    base_path = kwargs.get('base_path', '')
    full_path = os.path.join(base_path, path)

    if not os.path.exists(full_path):
        os.mkdir(full_path)


def create_file(test_case, kwargs):
    base_path = kwargs.get('base_path', '')
    full_path = os.path.join(base_path, test_case[0])

    with open(full_path, 'w') as file:

        for line in test_case[1]:
            file.write(line)


def save_problem_cases(path, problem, **kwargs):

    def create_path(problem_id, consecutive, type):
        file_name = FILE_NAME_FORMAT.format(
            problem_id,
            consecutive,
            INPUT_SUFFIX if type else OUTPUT_SUFFIX
        )

        return "{}/{}".format(path, file_name)

    def to_list():

        consecutive = -1
        for test_case in problem.testCases:

            consecutive += 1

            input_file = create_path(
                problem.id,
                consecutive,
                True
            )

            output_file = create_path(
                problem.id,
                consecutive,
                False
            )

            yield input_file, test_case.input
            yield output_file, test_case.output

    create_folder(path, **kwargs)

    with ThreadPoolExecutor(max_workers=5) as executor:
        ex = executor.map(create_file, to_list(), repeat(kwargs))
        # TODO: Handle possible errors
