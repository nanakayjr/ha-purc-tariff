from pathlib import Path

from custom_components.purc_tariff.purc_client import PURCClient

FIXTURES_DIR = Path(__file__).parent / "fixtures"


def test_tariff_parser():

    html = (
        FIXTURES_DIR / "residential_100.html"
    ).read_text()


    client = PURCClient(
        "Residential"
    )


    result = client._parse(
        html
    )


    assert result["energy"] == 203.75
    assert result["levy"] == 10.19
    assert result["service"] == 10.73