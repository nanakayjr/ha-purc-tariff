import logging

from datetime import timedelta

from homeassistant.helpers.update_coordinator import (
    DataUpdateCoordinator,
    UpdateFailed,
)

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant


from .const import (
    SCAN_INTERVAL_HOURS,
    CONF_CUSTOMER_TYPE,
)

from .purc_client import PURCClient
from .exceptions import PURCError


_LOGGER = logging.getLogger(__name__)


class PURCCoordinator(
    DataUpdateCoordinator
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


        super().__init__(
            hass,
            _LOGGER,
            config_entry=entry,
            name="PURC Tariff",
            update_interval=timedelta(
                hours=SCAN_INTERVAL_HOURS
            )
        )



    async def _async_update_data(
        self
    ):


        try:

            return await self.hass.async_add_executor_job(
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


        return data