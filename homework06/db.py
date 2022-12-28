from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()
engine = create_engine("sqlite:///news.db")
session = sessionmaker(bind=engine)


class News(Base):
    __tablename__ = "news"
    id = Column(Integer, primary_key=True)
    title = Column(String)
    author = Column(String)
    url = Column(String)
    comments = Column(Integer)
    points = Column(Integer)
    label = Column(String)

    @staticmethod
    def update_news(m):
        s = session()
        for i in m:
            if not s.query(News).filter(News.title == i["title"], News.author == i["author"]).first():
                s.add(News(**i))
        s.commit()

    @staticmethod
    def add_label(id, label):
        s = session()
        s.query(News).get(id).label = label
        s.commit()

    @staticmethod
    def get(label):
        return session().query(News).filter(News.label != None if label else News.label == None).all()

Base.metadata.create_all(bind=engine)
