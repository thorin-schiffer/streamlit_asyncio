
from beanie import init_beanie, Document


class Product(Document):
    name: str
async def init_database(client):
    database = client.get_database(name='asyncio_streamlit_db')
    await init_beanie(database=database, document_models=[Product])