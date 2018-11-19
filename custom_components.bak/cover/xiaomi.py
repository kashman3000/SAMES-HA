"""
Support for Xiaomi curtain.

Developed by Schumyhao (bob-hjl@126.com)
"""
import logging

from homeassistant.components.cover import (
    CoverDevice, SUPPORT_OPEN, SUPPORT_CLOSE, SUPPORT_SET_POSITION)
from homeassistant.const import (
    ATTR_FRIENDLY_NAME, STATE_OPEN, STATE_CLOSED,
    ATTR_ENTITY_ID, CONF_COVERS, CONF_DEVICE_CLASS)
try:
    from homeassistant.components.xiaomi import (PY_XIAOMI_GATEWAY, XiaomiDevice)
except ImportError:
    from custom_components.xiaomi import (PY_XIAOMI_GATEWAY, XiaomiDevice)

_LOGGER = logging.getLogger(__name__)

ATTR_CURTAIN_LEVEL = 'curtain_level' # Curtain position in total rail lentgh (%)

def setup_platform(hass, config, add_devices, discovery_info=None):
    """Perform the setup for Xiaomi devices."""
    devices = []
    gateways = PY_XIAOMI_GATEWAY.gateways
    for (ip_add, gateway) in gateways.items():
        for device in gateway.devices['cover']:
            model = device['model']
            if model == 'curtain':
                devices.append(XiaomiGenericCover(device, "Curtain",
                    {'status': 'status', 'pos': 'curtain_level'}, gateway))
    add_devices(devices)


class XiaomiGenericCover(XiaomiDevice, CoverDevice):
    """Representation of a XiaomiPlug."""

    def __init__(self, device, name, data_key, xiaomi_hub):
        """Initialize the XiaomiPlug."""
        self._state = False
        self._data_key = data_key
        self._pos = 0
        XiaomiDevice.__init__(self, device, name, xiaomi_hub)

    @property
    def current_cover_position(self):
        """Return the current position of the cover."""
        return self._pos

    @property
    def is_closed(self):
        """Return if the cover is closed."""
        if self.current_cover_position > 0:
            return False
        else:
            return True

    def close_cover(self, **kwargs):
        """Close the cover."""
        self.xiaomi_hub.write_to_hub(self._sid,
            self._data_key['status'], 'close')

    def open_cover(self, **kwargs):
        """Open the cover."""
        self.xiaomi_hub.write_to_hub(self._sid,
            self._data_key['status'], 'open')

    def stop_cover(self, **kwargs):
        """Stop the cover."""
        self.xiaomi_hub.write_to_hub(self._sid,
            self._data_key['status'], 'stop')

    def set_cover_position(self, position, **kwargs):
        """Move the cover to a specific position."""
        self.xiaomi_hub.write_to_hub(self._sid,
            self._data_key['pos'], str(position))

    def parse_data(self, data):
        """Parse data sent by gateway"""
        if ATTR_CURTAIN_LEVEL in data:
            self._pos = int(data[ATTR_CURTAIN_LEVEL])
            return True
        return False
