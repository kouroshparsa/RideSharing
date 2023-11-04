import sys
import maskpass
import requests
import argparse
from rich.console import Console
from rich.table import Table
from inputimeout import inputimeout, TimeoutOccurred


def display_candidates(candidates):
    console = Console()
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Booking ID")
    table.add_column("Driver ID")
    table.add_column("Verhicle Type")
    table.add_column("Price")
    table.add_column("Rating")
    for candidate in candidates:
        table.add_row(candidate["booking_id"], candidate["driver_id"], candidate["vehicle_type"], candidate["price"], candidate["rating"])
    console.print(table)

parser = argparse.ArgumentParser(description='The url for the back-end server')
parser.add_argument('-u', '--url', required=True)

args = parser.parse_args()
url = args.url
email = input('Enter your email address:')
password = maskpass.askpass()

headers = {'Content-Type' : 'application/x-www-form-urlencoded'}
data = {'username': email, 'password': password}
res = requests.post(url + '/token/rider', data=data, headers=headers)
if res.status_code != 200:
    raise Exception(res.text)

access_token = res.json()['access_token']
print(f'access_token={access_token}')

org_address = input('Enter where you are:')
dst_address = input('Enter where you want to go:')

headers = {'Authorization': f'Bearer {access_token}'}
res = requests.get(f'{url}/address_to_geolocation/{org_address}', headers=headers)
if res.status_code != 200:
    raise Exception(res.text)

org_loc = res.json()


res = requests.get(f'{url}/address_to_geolocation/{dst_address}', headers=headers)
if res.status_code != 200:
    raise Exception(res.text)

dst_loc = res.json()

print(f'org_loc={org_loc} dst_loc={dst_loc}')

data = {"origin": org_loc, "destination": dst_loc, "origin_address": org_address, "destination_address": dst_address}
res = requests.get(f'{url}/trip_candidates', json=data, headers=headers)
if res.status_code != 200:
    raise Exception(res.text)

candidates = res.json()
if len(candidates) < 1:
    print('Sorry. There are no drivers near you.')
    sys.exit(0)

print('Here are your ride options:')
display_candidates(candidates)

booking_id = None
while booking_id is None:
    booking_id = input('Choose a ride (booking_id):').strip()
    if booking_id not in [candidate["booking_id"] for candidate in candidates]:
        print("Invalid booking_id")
        booking_id = None


print('Booking...')
res = requests.get(f'{url}/book/{booking_id}', headers=headers)

TOTAL_WAIT = 200 # seconds
CHECK_PERIOD = 5
print('Waiting for your ride...You can cancel by pressing "C"')
for _ in range(0, int(TOTAL_WAIT/CHECK_PERIOD)):
    try:
        res = inputimeout(timeout=5)
        if res.lower() == 'c':
            sys.exit(0)
    except TimeoutOccurred:
        res = requests.get(f'{url}/driver/{driver_id}', headers=headers)
        if res.status_code != 200:
            raise Exception(res.text)
        
        print(f"status={res.json()['status']}")
        if res.json()["status"] == "in_transit":
            print("You are picked up. Bye")
    
print('Done')