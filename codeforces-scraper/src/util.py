
class TestCase:

    def __init__(self, input, output):
        self.input = input
        self.output = output

    def __str__(self):

        cad = "Input:\n{}\nOutput:\n{}\n{sep}".format(
            self.input,
            self.output,
            sep=50 * '_'
        )

        return cad


class Problem:

    def __init__(self, id, url, contest_id):
        self.id = id
        self.url = url
        self.testCases = []
        self.contest = contest_id

    def __str__(self):
        return "{}: {}".format(self.id, self.url)
