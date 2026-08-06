import voluptuous as vol

from homeassistant import config_entries

from .const import (
    DOMAIN,
    CUSTOMER_TYPES,
    CONF_CUSTOMER_TYPE,
)



class PURCConfigFlow(
    config_entries.ConfigFlow,
    domain=DOMAIN,
):


    VERSION = 1


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

            return self.async_create_entry(
                title=user_input[
                    CONF_CUSTOMER_TYPE
                ],
                data=user_input
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
                    )

                }
            )
        )