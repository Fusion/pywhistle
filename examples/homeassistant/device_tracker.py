import logging
from datetime import timedelta
import voluptuous as vol
from homeassistant.helpers import aiohttp_client, config_validation as cv
from homeassistant.components.device_tracker import PLATFORM_SCHEMA
from homeassistant.const import (
    CONF_USERNAME, CONF_MONITORED_VARIABLES, CONF_PASSWORD, ATTR_ENTITY_PICTURE)
from homeassistant.helpers.event import async_track_time_interval


_LOGGER = logging.getLogger(__name__)
DEVICE_TYPES = ['WHISTLE']
PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Required(CONF_USERNAME): cv.string,
    vol.Required(CONF_PASSWORD): cv.string,
    vol.Optional(ATTR_ENTITY_PICTURE, default='60x60'): cv.string,
    vol.Optional(CONF_MONITORED_VARIABLES, default=DEVICE_TYPES):
        vol.All(cv.ensure_list, [vol.In(DEVICE_TYPES)]),
})


async def async_setup_scanner(hass, config, async_see, discovery_info=None):
    from pywhistle import Client

    websession = aiohttp_client.async_get_clientsession(hass)
    client = Client(
        config[CONF_USERNAME],
        config[CONF_PASSWORD],
        websession
    )
    scanner = WhistleScanner(
        client,
        hass,
        async_see,
        config[ATTR_ENTITY_PICTURE]
    )
    return await scanner.async_init()


class WhistleScanner:


    def __init__(self, client, hass, async_see, preferred_picture):
        self._preferred_picture = preferred_picture
        self._async_see = async_see
        self._client = client
        self._hass = hass


    async def async_init(self):
        try:
            await self._client.async_init()
        except Exception as e:
             _LOGGER.error('Unable to set up Tile scanner: %s', e)
             return False
        await self._async_update()
        async_track_time_interval(
            self._hass, self._async_update, timedelta(minutes=2))
        return True


    async def _async_update(self, now=None):
        _LOGGER.info('Updating Whistle data')
        try:
            await self._client.async_init()
            pets = await self._client.get_pets()
        except Exception as e:
            _LOGGER.error("There was an error while updating: %s", e)
        _LOGGER.debug("Retrieved data:")
        _LOGGER.debug(pets)
        if not pets:
            _LOGGER.warning("No Pets found")
            return
        for pet in pets['pets']:
            attributes = {
                'name': pet['name'],
                'battery_level': pet['device']['battery_level'],
                'battery_status': pet['device']['battery_status'],
                'pending_locate': pet['device']['pending_locate'],
                'activity_streak': pet['activity_summary']['current_streak'],
                'activity_minutes_active': pet['activity_summary']['current_minutes_active'],
                'activity_minutes_rest': pet['activity_summary']['current_minutes_rest'],
                'activity_goal': pet['activity_summary']['current_activity_goal']['minutes']
            }
            if self._preferred_picture in pet['profile_photo_url_sizes']:
                attributes['picture'] = pet['profile_photo_url_sizes'][self._preferred_picture]
            await self._async_see(
                dev_id = "whistle_%s" % ''.join(c for c in pet['name'] if c.isalnum()),
                gps = (
                    pet['last_location']['latitude'],
                    pet['last_location']['longitude']
                ),
                attributes = attributes,
                icon='mdi:view-grid')
