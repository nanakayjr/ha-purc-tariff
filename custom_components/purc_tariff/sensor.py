from __future__ import annotations

from homeassistant.components.sensor import (
    SensorEntity,
    SensorDeviceClass,
    SensorStateClass,
)

from homeassistant.config_entries import ConfigEntry

from homeassistant.core import HomeAssistant

from homeassistant.helpers.entity_platform import (
    AddEntitiesCallback,
)

from homeassistant.helpers.update_coordinator import (
    CoordinatorEntity,
)

from .const import (
    CONF_CUSTOMER_TYPE,
    CONF_TRACK_WATER,
    DECIMAL_PRECISION,
    DOMAIN,
)

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


    entities = []


    customer_type = (
        entry.data[CONF_CUSTOMER_TYPE]
    )


    if customer_type == "Residential":

        entities.extend(
            [

                PURCSensor(
                    coordinator,
                    entry,
                    "lifeline_tariff",
                    "Lifeline Tariff",
                    "GHS/kWh",
                ),


                PURCSensor(
                    coordinator,
                    entry,
                    "lifeline_service",
                    "Lifeline Service Charge",
                    "GHS",
                ),


                PURCSensor(
                    coordinator,
                    entry,
                    "regular_tariff",
                    "Regular Consumer Tariff",
                    "GHS/kWh",
                ),


                PURCSensor(
                    coordinator,
                    entry,
                    "high_tariff",
                    "High Consumer Tariff",
                    "GHS/kWh",
                ),


                PURCSensor(
                    coordinator,
                    entry,
                    "levy",
                    "Levy Tax",
                    "%",
                ),


                PURCSensor(
                    coordinator,
                    entry,
                    "regular_service",
                    "Regular/High Consumer Service Charge",
                    "GHS",
                ),

            ]
        )


    else:

        entities.extend(
            [

                PURCSensor(
                    coordinator,
                    entry,
                    "regular_tariff",
                    "Regular Consumer Tariff",
                    "GHS/kWh",
                ),


                PURCSensor(
                    coordinator,
                    entry,
                    "high_tariff",
                    "High Consumer Tariff",
                    "GHS/kWh",
                ),


                PURCSensor(
                    coordinator,
                    entry,
                    "levy",
                    "Levy Tax",
                    "%",
                ),


                PURCSensor(
                    coordinator,
                    entry,
                    "regular_service",
                    "Regular/High Consumer Service Charge",
                    "GHS",
                ),

            ]
        )


    if entry.data.get(CONF_TRACK_WATER):

        entities.extend(
            [

                PURCSensor(
                    coordinator,
                    entry,
                    "water_tariff",
                    "Water Tariff",
                    "GHS/m\u00b3",
                ),


                PURCSensor(
                    coordinator,
                    entry,
                    "water_service",
                    "Water Service Charge",
                    "GHS",
                ),


                PURCSensor(
                    coordinator,
                    entry,
                    "water_levy",
                    "Water Levy",
                    "%",
                ),

            ]
        )


    entities.append(
        PURCLastUpdatedSensor(
            coordinator,
            entry
        )
    )


    async_add_entities(
        entities
    )



class PURCSensor(
    CoordinatorEntity,
    SensorEntity
):


    _attr_has_entity_name = True


    def __init__(
        self,
        coordinator: PURCCoordinator,
        entry: ConfigEntry,
        key: str,
        name: str,
        unit: str,
    ):

        super().__init__(
            coordinator
        )


        self.key = key


        self._attr_name = name


        self._attr_unique_id = (
            f"{entry.entry_id}_{key}"
        )


        self._attr_native_unit_of_measurement = (
            unit
        )


        self._attr_device_info = build_device_info(entry)



        if unit == "GHS/kWh":

            self._attr_icon = (
                "mdi:currency-usd"
            )


            self._attr_state_class = (
                SensorStateClass.MEASUREMENT
            )


        elif unit == "GHS/m\u00b3":

            self._attr_icon = (
                "mdi:water"
            )


            self._attr_state_class = (
                SensorStateClass.MEASUREMENT
            )


        elif unit == "%":

            self._attr_icon = (
                "mdi:percent"
            )


            self._attr_state_class = (
                SensorStateClass.MEASUREMENT
            )


        else:

            self._attr_icon = (
                "mdi:cash"
            )

            self._attr_device_class = (
                SensorDeviceClass.MONETARY
            )

            self._attr_state_class = (
                SensorStateClass.MEASUREMENT
            )



    @property
    def native_value(self):

        if not self.coordinator.data:

            return None


        value = self.coordinator.data.get(
            self.key
        )

        if value is None:
            return None


        return round(
            value,
            DECIMAL_PRECISION
        )


class PURCLastUpdatedSensor(
    CoordinatorEntity,
    SensorEntity
):


    _attr_has_entity_name = True

    _attr_name = "Last Updated"

    _attr_icon = "mdi:clock-check-outline"

    _attr_device_class = SensorDeviceClass.TIMESTAMP


    def __init__(
        self,
        coordinator: PURCCoordinator,
        entry: ConfigEntry,
    ):

        super().__init__(
            coordinator
        )

        self._attr_unique_id = (
            f"{entry.entry_id}_last_updated"
        )

        self._attr_device_info = build_device_info(entry)


    @property
    def native_value(self):

        return self.coordinator.last_update_success_time