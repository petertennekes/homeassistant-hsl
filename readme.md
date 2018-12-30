copy src/sensor/hsl.py to config/custom_components/sensor/
copy src/frontend/* to config/www/

add
sensor:
  platform: hsl
to configuration..yaml

add 
resources:
  - type: module
    url: /local/hsl-card.js
  - type: js
    url: 'https://unpkg.com/moment@2.22.2/moment.js'

 - entity: sensor.hsl_sensor
   type: 'custom:hsl-card'

to ui-lovelace.yaml

