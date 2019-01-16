import os

from concurrent.futures import ThreadPoolExecutor


INPUT_SUFFIX = 'input'
OUTPUT_SUFFIX = 'output'
FILE_NAME_FORMAT = "{}_{}.{}"


def create_folder(path):

    if not os.path.exists(path):
        os.mkdir(path)


def create_file(test_case):
    with open(test_case[0], 'w') as file:

        for line in test_case[1]:
            file.write(line)


def save_problem_cases(path, problem):

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

    create_folder(path)

    with ThreadPoolExecutor(max_workers=5) as executor:
        executor.map(create_file, to_list())
