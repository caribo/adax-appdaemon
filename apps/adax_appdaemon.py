# Load energy figures from the Adax API
#
# Args: adax_client, adax_secret
#

import appdaemon.plugins.hass.hassapi as hass
from datetime import datetime, timezone
import requests
import json

class AdaxEnergy(hass.Hass):

    def initialize(self):
        self.log('Adax Energy started')
        self.set_namespace('hass')
        self.run_in(self.update, 0)
        # update every 5 minutes
        self.run_every(self.update, datetime.now(), 300)

    def get_token(self):
        adax_client = self.args['adax_client']
        adax_secret = self.args['adax_secret']
        adax_token_url = 'https://api-1.adax.no/client-api/auth/token'
        data = {'username': adax_client, 'password': adax_secret, 'grant_type': 'password'}
        response = requests.post(adax_token_url, data=data)
        response.raise_for_status()
        if response.status_code == 200:
            json = response.json()
            if ('access_token' in json):
                return json['access_token']
        raise ApiException('Token not returned from Adax API')

    def get_devices(self,token):
        adax_api_url = 'https://api-1.adax.no/client-api/rest/v1/content/?withEnergy=1'
        headers = { 'Authorization': 'Bearer ' + token }
        response = requests.get(adax_api_url, headers = headers)
        response.raise_for_status()
        if response.status_code == 200:
            json = response.json()
            if ('devices' in json):
                return json['devices']
        raise ApiException('No devices returned from Adax API')

    def update(self, kwargs):
        self.log('Adax Energy update started')
        token = self.get_token()
        devices = self.get_devices(token)
        for device in devices:
            deviceName = device['name']
            friendlyName = f'Adax heater - {deviceName}'
            sensor = f'sensor.adax_{deviceName.replace(" ","_").replace(".","_").lower()}_energy'
            epochTime = (device['energyTime'] / 1000);
            energyTime = datetime.fromtimestamp(epochTime, tz=timezone.utc).strftime('%Y-%m-%d %H:%M:%S')
            energy = device['energyWh'];
            self.log(f'{energyTime}, {deviceName}, {energy}')
            self.set_state(entity_id = sensor,
                friendly_name = friendlyName,
                device_class = 'energy',
                state_class = 'total_increasing',
                unit_of_measurement = 'Wh',
                state = energy,
                energy_time = energyTime)

