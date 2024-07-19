from typing import Awaitable
import xml.etree.ElementTree as et



async def xml_to_dict(xml_message: bytes) -> Awaitable[dict]:
    '''
    response example format:
{
    AUD: {
            data: {
                VunitRate: float
                Nominal: int,
            },
            meta: {
                    ID: str,
                    NumCode: str,
                    Name: str,
                    Value: float
                    
            }
        }
}
'''
    root = et.fromstring(xml_message)
    result = {}

    for valute in root.findall('Valute'):            
        if char_code := valute.find('CharCode').text:
            result[char_code] = {
                "data": {
                    "VunitRate": float(valute.find('VunitRate').text.replace(',', '.')),
                    "Nominal": int(valute.find('Nominal').text)
                },
                "meta": {
                    "ID":  valute.attrib.get('ID'),
                    "NumCode": valute.find('NumCode').text,
                    "Name": valute.find('Name').text,
                    "Value": float(valute.find('Value').text.replace(',', '.'))
                }
            }
    
    return result
