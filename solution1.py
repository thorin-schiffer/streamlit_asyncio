import asyncio

from beanie import Document, init_beanie
from motor.motor_asyncio import AsyncIOMotorClient
import streamlit as st


def get_client(event_loop=None):
    if event_loop:
        client = AsyncIOMotorClient(
            "mongodb://127.0.0.1:27017/?directConnection=true&serverSelectionTimeoutMS=2000&appName=mongosh+2.0.2",
            io_loop=event_loop,
        )
    else:
        client = AsyncIOMotorClient(
            "mongodb://127.0.0.1:27017/?directConnection=true&serverSelectionTimeoutMS=2000&appName=mongosh+2.0.2",
        )
    return client


class Product(Document):
    name: str


async def init_database(client):
    database = client.get_database(name='asyncio_streamlit_db')
    await init_beanie(database=database, document_models=[Product])


async def fetch_data():
    count = await Product.find(fetch_links=True).count()
    if not count:
        await Product(name='test').save()
    await asyncio.sleep(5)
    return await Product.find(fetch_links=True).to_list()


async def main():
    client = get_client()
    await init_database(client)
    products = await fetch_data()
    for product in products:
        st.write(product)


if __name__ == '__main__':
    asyncio.run(main())
