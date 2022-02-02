"""Constants for Compare It integration."""
from datetime import timedelta

DOMAIN = "compareit"
SCAN_INTERVAL = timedelta(seconds=30)
PLATFORMS = ["light"]
DOMAIN_DATA = f"{DOMAIN}_data"