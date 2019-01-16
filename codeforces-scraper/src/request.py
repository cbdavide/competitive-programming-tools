from requests import get
from contextlib import closing


def get_html(url):

    with closing(get(url, stream=True)) as req:
        if req.status_code != 200:
            return None

        cnt_type = req.headers.get('Content-Type', '')
        cnt_type = cnt_type.lower()

        if 'html' not in cnt_type:
            return None

        return req.content

if __name__ == '__main__':

    print(
        get_html('https://codeforces.com/problemset/problem/1099/Z')
    )
