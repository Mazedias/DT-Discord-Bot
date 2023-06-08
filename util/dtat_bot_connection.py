import requests
import json


def http_req(guild_id) -> dict:
    response = requests.get(f'https://dtat.hampl.space/data/guild/id/{guild_id}/data')
    return json.loads(response.text)
