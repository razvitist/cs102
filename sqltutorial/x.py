# import re

# train = [
#     ('I love this sandwich.', 'pos'),
#     ('This is an amazing place!', 'pos'),
#     ('I feel very good about these beers.', 'pos'),
#     ('This is my best work.', 'pos'),
#     ("What an awesome view", 'pos'),
#     ('I do not like this restaurant', 'neg'),
#     ('I am tired of this stuff.', 'neg'),
#     ("I can't deal with this", 'neg'),
#     ('He is my sworn enemy!', 'neg'),
#     ('My boss is horrible.', 'neg')
# ]
# # test = [
# #     ('The beer was good.', 'pos'),
# #     ('I do not enjoy my job', 'neg'),
# #     ("I ain't feeling dandy today.", 'neg'),
# #     ("I feel amazing!", 'pos'),
# #     ('Gary is a friend of mine.', 'pos'),
# #     ("I can't believe I'm doing this.", 'neg')
# # ]

# d = {}
# posneg = [0, 0]
# for i in train:
#   m = re.sub(r'[^\w\s]', '', i[0]).lower().split()
#   state = i[1] == 'neg'
#   for j in m:
#     if not j in d:
#       d[j] = [0, 0]
#     d[j][state] += 1
#     posneg[state] += 1
# print(d)
# print(posneg, len(d))

import sqlalchemy as db
from pprint import pprint

engine = db.create_engine('sqlite:///testik.db')

connection = engine.connect()

metadata = db.MetaData()

products = db.Table('products', metadata,
  db.Column('id', db.Integer, primary_key=True),
  db.Column('name', db.Text),
  db.Column('price', db.Integer),
)

metadata.create_all(engine)

insertion = products.insert().values([
  {'name': 'Banana', 'price': 1000},
  {'name': 'Apple', 'price': 1200}
])

# connection.execute(insertion)

def printdb():
  select_q = db.select([products]) # .where(products.columns.price == 1200)
  select_r = connection.execute(select_q)
  pprint(select_r.fetchall())

printdb()

update_q = db.update(products).where(products.columns.price == 1000).values(price = 1500)
connection.execute(update_q)

printdb()

delete_q = db.delete(products).where(products.columns.id == 5)
connection.execute(delete_q)

printdb()