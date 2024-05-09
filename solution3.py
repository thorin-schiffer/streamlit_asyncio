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

COUNT = 10

async def fetch_data():
    count = await Product.find(fetch_links=True).count()
    if count < COUNT:
        for i in range(COUNT):
            await Product(name='test').save()
    await asyncio.sleep(5)
    return await Product.find(fetch_links=True).limit(COUNT).to_list()

def get_event_loop():
    return asyncio.new_event_loop()


if not st.session_state.get('event_loop'):
    st.session_state.event_loop = get_event_loop()

if not st.session_state.get('client'):
    st.session_state.client = get_client(event_loop=st.session_state.event_loop)

async def main():
    await init_database(st.session_state.client)
    products = await fetch_data()
    for product in products:
        st.write(product)
    st.button("Quick rerun")

if __name__ == '__main__':
    st.session_state.event_loop.run_until_complete(main())
