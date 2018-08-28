# Задача:
# Доделать все тот же многопоточный парсер, только можно без класса.
# Просто на 2-х функциях: одна является обработчиком, именно она
# работает многопоточно, а вторая - стартует потоки.


import sqlalchemy as sa


TABLE_NAME = 'kondyurin_crawler'


metadata = sa.MetaData()
connection = {'user': 'py4seo', 'database': 'library', 'host': '46.30.164.249', 'password': 'PY1111forSEO'}
dsn = 'postgresql://{user}:{password}@{host}/{database}'.format(**connection)
engine = sa.create_engine(dsn)
metadata.bind = engine

domain = sa.Table(
    TABLE_NAME, metadata,
    sa.Column('id', sa.Integer, primary_key=True),
    sa.Column('domain', sa.String(255)),
    sa.Column('url', sa.Text),
    sa.Column('title', sa.Text),
    sa.Column('description', sa.Text),
    sa.Column('h1', sa.Text)
)


if __name__ == '__main__':
    metadata.create_all()