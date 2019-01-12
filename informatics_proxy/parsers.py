import bs4
import re

user_id_regex = re.compile('user_id=([0-9]+)')


def parse_standings_problem(s: str):
    s = s.strip()
    if s == '':
        return 0
    elif s == '+':
        return 1
    elif s == '-':
        return -1
    else:
        return int(s)


def parse_standings(html: str):
    soup = bs4.BeautifulSoup(html, 'html.parser')
    tables = soup.find_all('table', class_='BlueTable')
    standings = tables[0]
    rows = standings.find_all('tr', recursive=False)

    for row in rows[1:]:
        place_wrapper = row.find_all('td', recursive=False)[0]
        user_wrapper = place_wrapper.find_all('td', recursive=False)[0]
        user = user_wrapper.find('a')
        rest = user_wrapper.find_all('td')

        user_id = int(user_id_regex.findall(user['href'])[0])

        *problems, total, penalty = rest
        problems = [
            parse_standings_problem(p.text)
            for p in problems
        ]
        total = int(total.text)
        penalty = int(penalty.text)

        yield {
            'user': {
                'id': user_id,
                'name': user.text,
            },
            'problems': problems,
            'total': int(total),
            'penalty': penalty,
        }
