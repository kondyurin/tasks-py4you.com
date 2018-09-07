import sqlalchemy as sa


TABLE_NAME = 'kondyurin_crawler_asyncio'


metadata = sa.MetaData()
connection = {'user': 'py4seo', 'database': 'library', 'host': '', 'password': ''}

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








# async def main():
#     engine = await gino.create_engine(dsn)
#     metadata.bind = engine
#
#
# if __name__ == '__main__':
#     metadata.create_all()
#     loop = asyncio.get_event_loop()
#     loop.run_until_complete(main())


# async def create_table(conn):
#     await conn.execute('DROP TABLE IF EXISTS domain')
#     await conn.execute('''CREATE TABLE domain (
#         id serial PRIMARY KEY,
#         domain varchar(255),
#         url varchar,
#         title varchar,
#         description varchar,
#         h1 varchar)''')


# async def go():
#     async with create_engine(dsn) as engine:
#         async with engine.acquire() as conn:
#             await create_table(conn)

# async def go():
#     engine = await create_engine(dsn)
#     async with engine:
#         async with engine.acquire() as conn:
#             await create_table(conn)

# engine = sa.create_engine(dsn)
#
# metadata.bind = engine
