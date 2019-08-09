copy src/hsl/* to config/custom_components/hsl/*
copy src/frontend/* to config/www/

add
sensor:
  - platform: hsl
    stop_id: HSL:294985

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

