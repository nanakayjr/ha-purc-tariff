import voluptuous as vol

from homeassistant import config_entries

from .const import (
    DOMAIN,
    CUSTOMER_TYPES,
    CONF_CUSTOMER_TYPE,
    CONF_TRACK_WATER,
    CONF_WATER_CUSTOMER_TYPE,
    WATER_CUSTOMER_TYPES,
)



class PURCConfigFlow(
    config_entries.ConfigFlow,
    domain=DOMAIN,
):


    VERSION = 1


    def __init__(self):

        self._data = {}


    async def async_step_user(
        self,
        user_input=None
    ):

        if user_input:

            await self.async_set_unique_id(
                user_input[
                    CONF_CUSTOMER_TYPE
                ]
            )

            self._abort_if_unique_id_configured()

            self._data.update(user_input)

            if user_input.get(CONF_TRACK_WATER):

                return await self.async_step_water()

            return self.async_create_entry(
                title=self._data[
                    CONF_CUSTOMER_TYPE
                ],
                data=self._data
            )


        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {

                    vol.Required(
                        CONF_CUSTOMER_TYPE,
                        default="Residential"
                    ):
                    vol.In(
                        CUSTOMER_TYPES
                    ),

                    vol.Optional(
                        CONF_TRACK_WATER,
                        default=False
                    ): bool,

                }
            )
        )


    async def async_step_water(
        self,
        user_input=None
    ):

        if user_input:

            self._data.update(user_input)

            return self.async_create_entry(
                title=self._data[
                    CONF_CUSTOMER_TYPE
                ],
                data=self._data
            )


        return self.async_show_form(
            step_id="water",
            data_schema=vol.Schema(
                {

                    vol.Required(
                        CONF_WATER_CUSTOMER_TYPE,
                        default="Residential"
                    ):
                    vol.In(
                        WATER_CUSTOMER_TYPES
                    )

                }
            )
        )