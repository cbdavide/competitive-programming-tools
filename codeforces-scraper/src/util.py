
class TestCase:

    def __init__(self, input_text, output_text):
        self.input = input_text
        self.output = output_text

    def __str__(self):

        cad = "Input:\n{}\nOutput:\n{}\n{sep}".format(
            self.input,
            self.output,
            sep=50 * '_'
        )

        return cad


class Problem:

    def __init__(self, problem_id, url):
        self.id = problem_id
        self.url = url
        self.testCases = []

    def __str__(self):
        return f"{self.id}: {self.url}"
