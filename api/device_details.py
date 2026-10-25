import requests as r
import logging

logger = logging.getLogger(__name__)

def fetch_details(machine_object, base_url: str, endpoint: str, auth_user: str, auth_password: str):
    response = r.get(f'{base_url}{endpoint}',
            auth=(auth_user,auth_password),
            timeout=30)
    response.raise_for_status()

    json_response = response.json()
    if json_response['msg'] != 'Successful operation':
        raise ValueError(f'API error: {json_response.get('msg')}')
    
    machine_object.stripe_status = json_response['cabinet']['posOnlineStatus']
    faults = []
    for slot in json_response['cabinet']['batcabs']:
        if slot['pFaultType'] != 0:
            faults.append(f'Slot {slot['pKakou']}: {slot['pFaultCause']}')

    machine_object.faults = faults
    