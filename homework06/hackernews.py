# fmt: off

from bayes import NaiveBayesClassifier
from bottle import redirect, request, route, run, template
from db import News, session
from scraputils import get_news


@route('/')
@route("/news")
def news_list():
    s = session()
    rows = s.query(News).filter(News.label == None).all()
    return template('news_template', rows=rows)


@route("/add_label/")
def add_label():
    News.add_label(request.query["id"], request.query["label"])
    redirect("/news")


@route("/update")
def update_news():
    news = get_news("https://news.ycombinator.com/newest")
    News.update_news(news)
    redirect("/news")


@route("/recommendations")
@route("/classify")
def classify_news():
    ...


if __name__ == "__main__":
    run(host="localhost", port=8080)
