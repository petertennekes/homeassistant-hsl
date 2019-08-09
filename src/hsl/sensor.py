import homeassistant.helpers.config_validation as cv
from homeassistant.helpers.entity import Entity
import voluptuous as vol
from homeassistant.const import CONF_NAME
from homeassistant.components.sensor import PLATFORM_SCHEMA
from datetime import timedelta, datetime
from homeassistant.util import Throttle
import logging

logger = logging.getLogger(__name__)


MIN_TIME_BETWEEN_UPDATES = timedelta(seconds=15)
CONF_STOP_ID = 'stop_id'
DEFAULT_NAME = 'hsl'

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Required(CONF_STOP_ID): cv.string,
    vol.Optional(CONF_NAME, default=DEFAULT_NAME): cv.string,
})

def setup_platform(hass, config, add_devices, discovery_info=None):
    """Setup the sensor platform."""
    logger.info("test")
    stop_id = config.get(CONF_STOP_ID)
    sensor_name = config.get(CONF_NAME)
    add_devices([HSLSensor(sensor_name, stop_id)])


class HSLSensor(Entity):
    """Representation of a Sensor."""

    def __init__(self, sensor_name, stop_id):
        """Initialize the sensor."""
        logger.info("init")
        self.sensor_name = sensor_name
        self.stop_id= stop_id
        self._state = None
        self._data = {}
        self.update()

    @property
    def name(self):
        """Return the name of the sensor."""
        return 'HSL Sensor'

    @property
    def state(self):
        """Return the state of the sensor."""
        return self._state

    @property
    def device_state_attributes(self):
        """Return device specific state attributes."""
        return {'route': self._data[0].get("route")}

    @Throttle(MIN_TIME_BETWEEN_UPDATES)
    def update(self):
        logger.info("updating:")

        """Fetch new state data for the sensor.

        This is the only method that should fetch new data for Home Assistant.
        """
        stop = Stop(self.stop_id)
        new_data = stop.update()
        self._data = new_data
        self._state = new_data[0]["departure"]
        logger.info("Done updating")


class Stop:
    def __init__(self, stop_id):
        from graphql_client import GraphQLClient
        self.client = GraphQLClient('https://api.digitransit.fi/routing/v1/routers/hsl/index/graphql')
        self.stop_id = stop_id

    def update(self):
        query_string = '''
            {
                  stop(id: "%s") {
                    gtfsId
                    name
                    lat
                    lon
                    stoptimesWithoutPatterns {
                      scheduledDeparture
                      realtimeDeparture
                      departureDelay
                      realtime
                      realtimeState
                      serviceDay
                      headsign
                      trip {
                        pattern {
                          code
                        }
                        routeShortName
                        alerts {
                          alertHeaderText
                        }
                        directionId
                      }

                    }
                    patterns {
                      code
                      directionId
                      headsign
                      route {
                        gtfsId
                        shortName
                        longName
                        mode
                      }
                    }
                  }
                }
            ''' % self.stop_id
        result = self.client.query(query_string)
        return self.parse_result(result)


    def parse_result(self, result):
        data = result.get("data")
        stop = data.get("stop")
        stop_name = stop.get("name")
        stop_activities = stop.get("stoptimesWithoutPatterns")
        departures = list(map(self.parse_stoptime, stop_activities))
        departures = list(filter(lambda x: x is not None, departures))
        return departures

    def parse_stoptime(self, stoptime):
        headsign = stoptime.get("headsign")
        departuretime_timestamp = stoptime.get("serviceDay") + stoptime.get("realtimeDeparture")
        departuretime = datetime.fromtimestamp(departuretime_timestamp)
        delay = stoptime.get("departureDelay")
        route = stoptime.get("trip").get("routeShortName")
        if headsign is not None:
            return {'sign': headsign, 'departure': departuretime, 'delay': delay, 'route': route, 'timestamp': departuretime_timestamp}
