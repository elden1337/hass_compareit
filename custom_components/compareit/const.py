"""Constants for Compare It integration."""
from datetime import timedelta

DOMAIN = "compareit"
SCAN_INTERVAL = timedelta(seconds=30)
PLATFORMS = ["light", "binary_sensor"]
DOMAIN_DATA = f"{DOMAIN}_data"

NAME = "name"
ON = "on"
OFF = "off"
VALUE = "value"
UUID = "uuid"
TYPESTR = "type"