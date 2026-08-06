from homeassistant.components.diagnostics import async_redact_data
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from .const import CONF_CUSTOMER_TYPE, DOMAIN

TO_REDACT = {
    CONF_CUSTOMER_TYPE,
}


async def async_get_config_entry_diagnostics(
    hass: HomeAssistant,
    entry: ConfigEntry,
) -> dict:
    coordinator = hass.data[DOMAIN][entry.entry_id]

    return {
        "customer": async_redact_data(entry.data, TO_REDACT),
        "last_update": (
            coordinator.last_update_success_time.isoformat()
            if coordinator.last_update_success_time
            else None
        ),
        "tariffs": coordinator.data,
    }
