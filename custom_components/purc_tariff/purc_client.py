import logging
import time

import requests

from bs4 import BeautifulSoup

from .const import PURC_URL, WATER_URL

from .exceptions import (
    PURCConnectionError,
    PURCParseError,
)


_LOGGER = logging.getLogger(__name__)


class _BaseClient:
    """Shared HTTP/retry/parsing logic for the PURC tariff reckoners."""


    def __init__(self):

        self.session = requests.Session()

        self.session.headers.update(
            {
                "User-Agent":
                "Home Assistant PURC Integration"
            }
        )



    def close(self):

        self.session.close()



    def calculate(
        self,
        consumption
    ):


        for attempt in range(3):

            try:

                return self._calculate(
                    consumption
                )

            except PURCParseError:
                raise

            except PURCConnectionError as err:

                if attempt == 2:
                    raise PURCConnectionError(
                        str(err)
                    )

                delay = 2 ** attempt

                _LOGGER.warning(
                    "PURC request failed, retrying in %s",
                    delay
                )

                time.sleep(delay)

        raise PURCConnectionError(
            "Unable to retrieve tariff data"
        )



    def _get_form_state(self, url):

        try:
            page = self.session.get(
                url,
                timeout=30
            )

        except requests.RequestException as err:
            raise PURCConnectionError(
                str(err)
            ) from err


        if page.status_code != 200:
            raise PURCConnectionError(
                f"Unexpected status code: {page.status_code}"
            )


        soup = BeautifulSoup(
            page.text,
            "html.parser"
        )


        viewstate = soup.find(
            "input",
            {
                "name":
                "__VIEWSTATE"
            }
        )


        eventvalidation = soup.find(
            "input",
            {
                "name":
                "__EVENTVALIDATION"
            }
        )


        if not viewstate or not eventvalidation:
            raise PURCParseError(
                "Missing ASP.NET form state fields"
            )


        return viewstate["value"], eventvalidation["value"]



    def _post(self, url, payload):

        try:
            response = self.session.post(
                url,
                data=payload,
                timeout=30
            )

        except requests.RequestException as err:
            raise PURCConnectionError(
                str(err)
            ) from err

        if response.status_code != 200:
            raise PURCConnectionError(
                f"Unexpected status code: {response.status_code}"
            )

        return response.text



    @staticmethod
    def _extract(soup, name):

        field = soup.find(
            id=f"MainContent_{name}"
        )


        if not field:
            raise PURCParseError(
                name
            )

        value = field.get("value")

        if value is None:
            raise PURCParseError(
                f"Missing value for {name}"
            )

        normalized = value.replace(",", "").strip()

        if not normalized:
            raise PURCParseError(
                f"Empty value for {name}"
            )

        try:
            return float(normalized)

        except ValueError as err:
            raise PURCParseError(
                f"Invalid numeric value for {name}: {value}"
            ) from err


class PURCClient(_BaseClient):
    """Client for the electricity tariff reckoner."""


    def __init__(
        self,
        customer_type
    ):

        super().__init__()

        self.customer_type = customer_type


    def _calculate(
        self,
        consumption
    ):

        viewstate, eventvalidation = self._get_form_state(
            PURC_URL
        )

        payload = {

            "__VIEWSTATE":
                viewstate,

            "__EVENTVALIDATION":
                eventvalidation,


            "ctl00$MainContent$ddlCustomerType":
                self.customer_type,


            "ctl00$MainContent$ddlCompPref":
                "Consumption (kWh)",


            "ctl00$MainContent$txtEConsmptn":
                str(consumption),


            "ctl00$MainContent$btnECalculate":
                "CALCULATE"
        }


        html = self._post(
            PURC_URL,
            payload
        )

        return self._parse(
            html
        )


    def _parse(
        self,
        html
    ):

        soup = BeautifulSoup(
            html,
            "html.parser"
        )

        return {

            "energy":
                self._extract(
                    soup,
                    "txtEnergyCharge"
                ),

            "levy":
                self._extract(
                    soup,
                    "txtLevyTax"
                ),

            "service":
                self._extract(
                    soup,
                    "txtESC"
                ),

            "total":
                self._extract(
                    soup,
                    "txtETotalAmt"
                )
        }


class PURCWaterClient(_BaseClient):
    """Client for the water tariff reckoner."""


    def __init__(
        self,
        customer_type
    ):

        super().__init__()

        self.customer_type = customer_type


    def _calculate(
        self,
        consumption
    ):

        viewstate, eventvalidation = self._get_form_state(
            WATER_URL
        )

        payload = {

            "__VIEWSTATE":
                viewstate,

            "__EVENTVALIDATION":
                eventvalidation,


            "ctl00$MainContent$ddlWCustomerType":
                self.customer_type,


            "ctl00$MainContent$ddlWCompPref":
                "Consumption (m3)",


            "ctl00$MainContent$txtVolumeConsumed":
                str(consumption),


            "ctl00$MainContent$btnWCalculate":
                "CALCULATE"
        }


        html = self._post(
            WATER_URL,
            payload
        )

        return self._parse(
            html
        )


    def _parse(
        self,
        html
    ):

        soup = BeautifulSoup(
            html,
            "html.parser"
        )

        return {

            "charge":
                self._extract(
                    soup,
                    "txtWaterCharge"
                ),

            "levy":
                self._extract(
                    soup,
                    "txtWLevy"
                ),

            "service":
                self._extract(
                    soup,
                    "txtWSC"
                ),

            "total":
                self._extract(
                    soup,
                    "txtWTotalAmount"
                )
        }