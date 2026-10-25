import requests as r
import logging

logger = logging.getLogger(__name__)

def fetch_id(machine_object, base_url: str, endpoint: str, auth_user: str, auth_password: str):
    response = r.get(f'{base_url}{endpoint}',
            auth=(auth_user,auth_password),
            timeout=30)
    response.raise_for_status()

    json_response = response.json()
    if json_response['msg'] != 'Successful operation':
        raise ValueError(f'API error: {json_response.get('msg')}')
    
    battery_quantity = 0
    battery_temperatures = []
    for value in json_response['data']:
        if value['pBatteryid'] is not None:
            battery_quantity += 1
        if value['pTemperature'] is not None:
            battery_temperatures.append(value['pTemperature'])

    machine_object.batteries = battery_quantity
    machine_object.max_battery_temperature = max(battery_temperatures, default=None)