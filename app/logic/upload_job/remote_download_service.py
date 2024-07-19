from typing import Awaitable, Callable
import httpx

async def get_date_from_bank(xml_formater: Callable[[bytes], Awaitable[dict]]) -> Awaitable[dict]:
    transport = httpx.AsyncHTTPTransport(retries=3)
    async with httpx.AsyncClient(transport=transport, timeout=8) as ac:
        response = await ac.get(url='https://cbr.ru/scripts/XML_daily.asp')
        assert response.status_code == 200
        xml_message = await response.aread()
        result = await xml_formater(xml_message)
        return result
