import logging

from datetime import timedelta

from homeassistant.helpers.event import async_track_time_interval
from homeassistant.helpers.storage import Store
from homeassistant.helpers.update_coordinator import (
    TimestampDataUpdateCoordinator,
    UpdateFailed,
)

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, callback

from homeassistant.util import dt as dt_util


from .const import (
    CONF_CUSTOMER_TYPE,
    CONF_TRACK_WATER,
    CONF_WATER_CUSTOMER_TYPE,
    DOMAIN,
    HEARTBEAT_INTERVAL_MINUTES,
    SCAN_INTERVAL_HOURS,
    STORAGE_VERSION,
    WATER_REFERENCE_CONSUMPTION,
)

from .purc_client import PURCClient, PURCWaterClient
from .exceptions import PURCError


_LOGGER = logging.getLogger(__name__)


class PURCCoordinator(
    TimestampDataUpdateCoordinator
):


    def __init__(
        self,
        hass: HomeAssistant,
        entry: ConfigEntry
    ):

        self.customer_type = (
            entry.data[CONF_CUSTOMER_TYPE]
        )


        self.client = PURCClient(
            self.customer_type
        )


        self.track_water = (
            entry.data.get(CONF_TRACK_WATER, False)
        )

        self.water_client = (
            PURCWaterClient(
                entry.data[CONF_WATER_CUSTOMER_TYPE]
            )
            if self.track_water
            else None
        )


        self._store = Store(
            hass,
            STORAGE_VERSION,
            f"{DOMAIN}_{entry.entry_id}"
        )


        super().__init__(
            hass,
            _LOGGER,
            config_entry=entry,
            name="PURC Tariff",
            update_interval=timedelta(
                hours=SCAN_INTERVAL_HOURS
            )
        )



    async def _async_setup(self) -> None:

        cached = await self._store.async_load()

        if cached:

            self.data = cached.get("data")

            last_updated = cached.get("last_updated")

            if last_updated:

                self.last_update_success_time = (
                    dt_util.parse_datetime(last_updated)
                )


        self.config_entry.async_on_unload(
            async_track_time_interval(
                self.hass,
                self._async_heartbeat,
                timedelta(minutes=HEARTBEAT_INTERVAL_MINUTES),
            )
        )



    @callback
    def _async_heartbeat(self, _now=None) -> None:
        """Re-announce the last known values so entities never look stale."""

        self.async_update_listeners()



    async def _async_update_data(
        self
    ):


        try:

            data = await self.hass.async_add_executor_job(
                self._discover
            )


        except PURCError as err:


            if self.data:

                _LOGGER.warning(
                    "Keeping previous tariff data after update failure: %s",
                    err
                )

                return self.data


            raise UpdateFailed(str(err)) from err


        await self._store.async_save(
            {
                "data": data,
                "last_updated": dt_util.utcnow().isoformat(),
            }
        )

        return data



    def _discover(self):


        data = {}


        if self.customer_type == "Residential":


            life = self.client.calculate(20)

            regular = self.client.calculate(100)

            high = self.client.calculate(400)


            data.update({

                "lifeline_tariff":
                    life["energy"] / 20,

                "lifeline_service":
                    life["service"],

                "regular_tariff":
                    regular["energy"] / 100,

                "high_tariff":
                    high["energy"] / 400,

                "regular_service":
                    regular["service"],

            })

            source = regular


        else:


            regular = self.client.calculate(100)

            high = self.client.calculate(400)


            data.update({

                "regular_tariff":
                    regular["energy"] / 100,

                "high_tariff":
                    high["energy"] / 400,

                "regular_service":
                    regular["service"],

            })

            source = regular



        data["levy"] = (
            source["levy"]
            /
            source["energy"]
            *
            100
        )


        if self.water_client is not None:

            water = self.water_client.calculate(
                WATER_REFERENCE_CONSUMPTION
            )

            data.update({

                "water_tariff":
                    water["charge"] / WATER_REFERENCE_CONSUMPTION,

                "water_service":
                    water["service"],

                "water_levy":
                    water["levy"] / water["charge"] * 100,

            })


        return data