# adax-appdaemon
Appdaemon app to load device energy readings for [Adax](https://adax.no/en/) heaters in Home Assistant.

## Configuration

**appdaemon.yaml** 

appdaemon.yaml needs to be configured to connect to your Home Assistant instance.

**secrets.yaml** 

secrets.yaml in your appdaemon folder should include secrets named adax_client & adax_secret corresponding to your Adax account ID (which can be found in your account in the Adax app) and an API secret which you can setup in 'Third party integrations / Remote API' in the adax app. When you choose to 'Add credential' the app will provide a password which is your API secret.

**apps.yaml**

Appdaemon's apps.yaml file should be configured to include the adax_appdaemon app:

```
adax:
  module: adax_appdaemon
  class: AdaxEnergy
  adax_client: !secret adax_client
  adax_secret: !secret adax_secret
```

## App

**adax_appdaemon.py**

adax_appdaemon.py integrates with the Adax API to obtain device energy consumption data every 5 minutes and updates energy sensors in Home Assistant.

The sensor state is the reading in Wh obtained from the Adax API. The device name will be modified to make it consumable in Home Assistant by replacing spaces and dots with underscores.

```
Sensor:                 sensor.adax_{deviceName}_energy
Friendly Name:          Aadax heater - {deviceName}
Device Class:           energy
State Class:            total_increasing
Unit of Measurement:    Wh
```

## Adax API

API details: https://adax.no/om-adax/api-development/

