from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from .const import (
    DOMAIN,
)

from .coordinator import PURCCoordinator


PLATFORMS = [
    "sensor",
]


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
):

    coordinator = PURCCoordinator(
        hass,
        entry
    )

    await coordinator.async_config_entry_first_refresh()

    hass.data.setdefault(
        DOMAIN,
        {}
    )

    hass.data[DOMAIN][entry.entry_id] = coordinator


    await hass.config_entries.async_forward_entry_setups(
        entry,
        PLATFORMS
    )

    return True



async def async_unload_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
):

    unload_ok = await hass.config_entries.async_unload_platforms(
        entry,
        PLATFORMS
    )

    if unload_ok:
        coordinator = hass.data[DOMAIN].pop(
            entry.entry_id,
            None
        )

        if coordinator is not None:
            coordinator.client.close()

        if not hass.data[DOMAIN]:
            hass.data.pop(DOMAIN)

    return unload_ok