"""Button platform for PURC Tariff."""

from __future__ import annotations

from homeassistant.components.button import ButtonEntity

from homeassistant.config_entries import ConfigEntry

from homeassistant.core import HomeAssistant

from homeassistant.helpers.entity_platform import (
    AddEntitiesCallback,
)

from homeassistant.helpers.update_coordinator import (
    CoordinatorEntity,
)

from .const import DOMAIN

from .coordinator import PURCCoordinator
from .device import build_device_info


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
):

    coordinator: PURCCoordinator = (
        hass.data[DOMAIN][entry.entry_id]
    )

    async_add_entities(
        [
            PURCForceUpdateButton(
                coordinator,
                entry
            )
        ]
    )


class PURCForceUpdateButton(
    CoordinatorEntity,
    ButtonEntity
):


    _attr_has_entity_name = True

    _attr_name = "Force Update"

    _attr_icon = "mdi:cloud-refresh"


    def __init__(
        self,
        coordinator: PURCCoordinator,
        entry: ConfigEntry,
    ):

        super().__init__(
            coordinator
        )

        self._attr_unique_id = (
            f"{entry.entry_id}_force_update"
        )

        self._attr_device_info = build_device_info(entry)


    async def async_press(self) -> None:
        """Force an immediate refresh from the PURC website."""

        await self.coordinator.async_request_refresh()
