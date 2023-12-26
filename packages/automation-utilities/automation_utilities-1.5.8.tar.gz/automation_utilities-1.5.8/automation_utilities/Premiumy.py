import requests


class Premiumy:
    def __init__(self, api_key: str):
        self.api_key = api_key

    def message(
            self,
            start_date: str = None,
            end_date: str = None,
            senderid: str = None,
            phone: str = None,
            page: int = 1,
            per_page: int = 15
    ):
        headers = {
            "Content-type": "application/json",
            "Api-Key": self.api_key
        }
        data = {
            "id": None,
            "jsonrpc": "2.0",
            "method": "sms.mdr_full:get_list",
            "params": {
                "filter": {
                    "start_date": start_date,
                    "end_date": end_date,
                    "senderid": senderid,
                    "phone": phone,
                },
                "page": page,
                "per_page": per_page,
            }
        }
        url = 'https://api.premiumy.net/v1.0/csv'

        response = requests.post(url=url, data=data, headers=headers)
        return response.json()