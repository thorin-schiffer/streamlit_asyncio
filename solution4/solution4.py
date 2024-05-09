import asyncio
from asyncio import run_coroutine_threadsafe
from threading import Thread
import os
import sys
from motor.motor_asyncio import AsyncIOMotorClient
import streamlit as st

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils import Product, init_database


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


@st.cache_resource(show_spinner=False)
def create_loop():
    loop = asyncio.new_event_loop()
    thread = Thread(target=loop.run_forever)
    thread.start()
    return loop, thread


st.session_state.event_loop, worker_thread = create_loop()


def run_async(coroutine):
    return run_coroutine_threadsafe(coroutine, st.session_state.event_loop).result()


@st.cache_resource(show_spinner=False)
def setup_database():
    if client := st.session_state.get("db_client"):
        return client
    client = get_client(event_loop=st.session_state.event_loop)
    run_async(init_database(client=client))
    return client


st.session_state.db_client = setup_database()


def main():
    products = run_async(fetch_data())
    for product in products:
        st.write(product)
    st.button("Quick rerun")


if __name__ == '__main__':
    main()
