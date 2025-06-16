import httpx
from .. import APIKeys

async def test_api():
    async with httpx.AsyncClient() as client:
        header = {
            "X-Api-Key" : APIKeys.key[0]
        }
        response = await client.get("https://stock.indianapi.in/stock?name=RELIANCE")
        assert response.status_code == 200
        with open ('response.json', 'w') as f:
            f.write(response.text)