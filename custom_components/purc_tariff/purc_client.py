import logging
import time

import requests

from bs4 import BeautifulSoup

from .const import PURC_URL

from .exceptions import (
    PURCConnectionError,
    PURCParseError,
)


_LOGGER = logging.getLogger(__name__)


class PURCClient:


    def __init__(
        self,
        customer_type
    ):

        self.customer_type = customer_type

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



    def _calculate(
        self,
        consumption
    ):


        try:
            page = self.session.get(
                PURC_URL,
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


        payload = {

            "__VIEWSTATE":
                viewstate["value"],

            "__EVENTVALIDATION":
                eventvalidation["value"],


            "ctl00$MainContent$ddlCustomerType":
                self.customer_type,


            "ctl00$MainContent$ddlCompPref":
                "Consumption (kWh)",


            "ctl00$MainContent$txtEConsmptn":
                str(consumption),


            "ctl00$MainContent$btnECalculate":
                "CALCULATE"
        }



        try:
            response = self.session.post(
                PURC_URL,
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


        return self._parse(
            response.text
        )



    def _parse(
        self,
        html
    ):


        soup = BeautifulSoup(
            html,
            "html.parser"
        )


        def extract(name):

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


        return {

            "energy":
                extract(
                    "txtEnergyCharge"
                ),

            "levy":
                extract(
                    "txtLevyTax"
                ),

            "service":
                extract(
                    "txtESC"
                ),

            "total":
                extract(
                    "txtETotalAmt"
                )
        }