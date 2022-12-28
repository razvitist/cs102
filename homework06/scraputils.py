# fmt: off

import requests
from bs4 import BeautifulSoup


def extract_news(parser):
    """ Extract news from a given web page """
    news_list = []
    m = {
        'author': parser.select('.hnuser'),
        'comments': parser.select('.subline > a:last-child'),
        'points': parser.select('span.score'),
        'title': parser.select('span.titleline > a'),
        'url': parser.select('span.titleline > a')
    }
    for i in range(30):
        comments = m['comments'][i].text.split()
        news_list.append({
            'author': m['author'][i].text,
            'comments': int(comments[0]) if len(comments) == 2 else 0,
            'points': int(m['points'][i].text.split()[0]),
            'title': m['title'][i].text,
            'url': m['url'][i]['href'],
        })
    return news_list


def extract_next_page(parser):
    """ Extract next page URL """
    return parser.select_one('.morelink')['href']


def get_news(url, n_pages=1):
    """ Collect news from a given web page """
    news = []
    while n_pages:
        print("Collecting data from page: {}".format(url))
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        news_list = extract_news(soup)
        next_page = extract_next_page(soup)
        url = "https://news.ycombinator.com/" + next_page
        news.extend(news_list)
        n_pages -= 1
    return news

# news_list = get_news("https://news.ycombinator.com/newest", n_pages=2)
# print(news_list)
# print(*(i['title'] for i in news_list), sep='\n')
# print(len(news_list))
