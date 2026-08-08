DOMAIN = "purc_tariff"

PURC_URL = (
    "https://www.purcghapp.com/Default.aspx"
)

WATER_URL = (
    "https://www.purcghapp.com/Water.aspx"
)

CONF_CUSTOMER_TYPE = "customer_type"
CONF_TRACK_WATER = "track_water_tariff"
CONF_WATER_CUSTOMER_TYPE = "water_customer_type"


CUSTOMER_TYPES = [
    "Residential",
    "Non-Residential",
    "SLT LV",
    "SLT MV",
    "SLT MV2",
    "SLT HV",
    "SLT EV Chg",
]


WATER_CUSTOMER_TYPES = [
    "Residential",
    "Non-Residential",
    "Commercial",
    "Sachet Water Producers",
    "Bottled Water and Drinks",
    "Industrial",
    "Public Inst./Gov. Depts.",
    "Public Stand Pipes",
    "Ports and Harbours",
    "Bulk Supply",
]

# Reference consumption (m3) used to derive the water tariff rate.
WATER_REFERENCE_CONSUMPTION = 100


SCAN_INTERVAL_HOURS = 24

# How often (in minutes) the last known sensor values are re-announced to
# Home Assistant so entities don't look stale between the daily refreshes.
HEARTBEAT_INTERVAL_MINUTES = 1

# Version of the on-disk cache used to persist the last known tariff data
# across Home Assistant restarts.
STORAGE_VERSION = 1

# Number of decimal places all numeric sensor values are rounded to.
DECIMAL_PRECISION = 2


DEVICE_NAME = (
    "PURC Electricity Tariff"
)