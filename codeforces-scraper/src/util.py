
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

    def __init__(self, id, url):
        self.id = id
        self.url = url
        self.testCases = []

    def __str__(self):
        return f"{self.id}: {self.url}"
