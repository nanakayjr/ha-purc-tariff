"""Shared device registry helpers."""

from __future__ import annotations

from homeassistant.config_entries import ConfigEntry

from .const import DEVICE_NAME, DOMAIN


def build_device_info(entry: ConfigEntry) -> dict:
    """Return the device info dict shared by all PURC entities."""

    return {

        "identifiers":
            {
                (
                    DOMAIN,
                    entry.entry_id
                )
            },

        "name":
            DEVICE_NAME,

        "manufacturer":
            "PURC Ghana",

        "model":
            "Tariff Reckoner",

    }
