import pytest
from httpx import AsyncClient

from ..db import database
from ..main import app

# Test if we miss one parameter
# Test an insert in private one image
# Test an insert in public bulk compare before and after of database^


@pytest.mark.asyncio
async def test_unsupported():
    """
    Unit test for making sure that our backend throws an error for unsupported file types
    """
    await database.connect()

    # files = [('files', ('image1', open('mock_data/image1.jpg', 'rb'), 'image/jpeg')),
    #          ('files', ('test', open('mock_data/test.pdf', 'rb'), 'application/pdf'))]

    async with AsyncClient(app=app, base_url="http://127.0.0.1:8000") as ac:
        response = await ac.post("/add/public/?api_key=stringstring&texts=string&texts=string&characteristics=string&characteristics=string", files=files)
        print(response.text)
    assert response.status_code == 400
    await database.disconnect()
