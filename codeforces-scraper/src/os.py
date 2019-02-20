import os
from itertools import repeat
from concurrent.futures import ThreadPoolExecutor


INPUT_SUFFIX = 'input'
OUTPUT_SUFFIX = 'output'
FILE_NAME_FORMAT = "{:02d}.{}"


class Persistence:

    def __init__(self, contest_id, **kwargs):
        self.template_file = kwargs.get('template', None)

        base_path = kwargs.get('base_path', '')
        self.path = os.path.join(base_path, contest_id)

    def save(self, problem):
        raise Exception('Not Implemented')


class DiskPersistence(Persistence):

    @staticmethod
    def _save_file(content, path):
        with open(path, 'w') as file:
            for line in content:
                file.write(line)

    def _save_test_case(self, test_case, consecutive, problem_id):

        # Saving test's case input
        file_name = FILE_NAME_FORMAT.format(consecutive, INPUT_SUFFIX)
        test_path = os.path.join(self.path, problem_id, file_name)

        self._save_file(test_case.input, test_path)

        # Saving test's case output
        file_name = FILE_NAME_FORMAT.format(consecutive, OUTPUT_SUFFIX)
        test_path = os.path.join(self.path, problem_id, file_name)

        self._save_file(test_case.output, test_path)

    def save(self, problem):
        problem_path = os.path.join(self.path, problem.id)

        # Make sure that the container folder exists
        os.makedirs(problem_path)

        with ThreadPoolExecutor(max_workers=5) as executor:
            ex = executor.map(
                self._save_test_case,
                problem.testCases,
                range(len(problem.testCases)),
                repeat(problem.id)
            )


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


def copy_file(input_file, output_path, problem_id, **kwargs):
    _, ext = os.path.splitext(input_file)

    base_path = kwargs.get('base_path', '')
    output_path = os.path.join(base_path, output_path, problem_id)

    output_path = f"{output_path}{ext}"

    with open(input_file) as template:

        with open(output_path, 'w') as output_file:

            for line in template:
                output_file.write(line)


def save_problem_cases(path, problem, **kwargs):

    def create_path(problem_id, consecutive, type):
        file_name = FILE_NAME_FORMAT.format(
            problem_id,
            consecutive,
            INPUT_SUFFIX if type else OUTPUT_SUFFIX
        )

        return f"{path}/{file_name}"

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

    template_path = kwargs.get('template_path', None)

    if template_path:
        copy_file(template_path, path, problem.id, **kwargs)

    with ThreadPoolExecutor(max_workers=5) as executor:
        ex = executor.map(create_file, to_list(), repeat(kwargs))
        # TODO: Handle possible errors
