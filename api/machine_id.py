import requests as r
import logging

logger = logging.getLogger(__name__)

def fetch_id(object_class, base_url: str, endpoint: str, auth_user: str, auth_password: str):
    response = r.get(f'{base_url}{endpoint}',
            auth=(auth_user,auth_password),
            timeout=30)
    response.raise_for_status()

    json_response = response.json()
    if json_response['msg'] != 'Successful operation':
        raise ValueError(f'API error: {json_response.get('msg')}')

    machine_identity = []
    for machine in json_response['data']:
        logger.info(f'{machine['pCabinetid']} found!')
        obj = object_class(cabinet_id=machine['pCabinetid'])
        if machine['pInfostatus'] == '在线':
            obj.status = 'Online'
        else:
            obj.status = 'Offline'

        machine_identity.append(obj)

    return machine_identity