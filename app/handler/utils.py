
from typing import Optional


def foramter_for_message(
    data: dict | list[dict],
    currency: Optional[str] = None,
    nominal: Optional[str] = None
    ):

    MAMAX_MESSAGE_LENGTH = 4096

    if isinstance(data, list):
        current_lenght = 0
        data = data[current_lenght:current_lenght + MAMAX_MESSAGE_LENGTH]

        result = []
        
        for (_, data_currency) in data:
            for key in data_currency:
                items_currency = data_currency[key]['data']
                result.append(f"1 {key} -> {items_currency['VunitRate'] / items_currency['Nominal']:.2f}\n")

        yield result

        current_lenght += MAMAX_MESSAGE_LENGTH
        result.clear()

    else:
        yield data[1][currency.upper()]['data']['VunitRate'] * float(nominal)
