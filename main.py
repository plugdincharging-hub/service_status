import logging
import os
from dotenv import load_dotenv
from dataclasses import dataclass, field

import api.machine_id as machine_id
import api.batteries as batteries
import api.device_details as device_details

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'),


load_dotenv()

def main():
    @dataclass
    class Machine:
        cabinet_id: str
        batteries: str | None = None
        status: str | None = None
        max_battery_temperature: int | None = None
        stripe_status: str | None = None
        faults: list[str] = field(default_factory=list)

    api_user = os.getenv('AUTH_USER')
    api_password = os.getenv('AUTH_PASSWORD')
    base_url = os.getenv('base_url')

    logging.info('Retrieving device identifications for future queries')
    machine_identity = machine_id.fetch_id(Machine, base_url,'/cabinet/getAllDevice', api_user, api_password) # Iteratively retrieve all active machines to query for more information

    for machine in machine_identity:
        batteries.fetch_id(machine, base_url, f'/cabinet/batteryListByCabinetId/{machine.cabinet_id}', api_user, api_password) # Retrieves all battery statuses and appends to machine object
        device_details.fetch_details(machine, base_url, f'/cabinet/detail/{machine.cabinet_id}', api_user, api_password) # Retrieves all stripe statuses and any detected faults and appends to machine object
        
if __name__ == '__main__':
    main()