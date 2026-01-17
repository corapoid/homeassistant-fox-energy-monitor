"""Constants for Fox Energy integration."""

DOMAIN = "fox_energy"
MANUFACTURER = "F&F"
DEFAULT_TIMEOUT = 30
DEFAULT_SCAN_INTERVAL = 5

# API Endpoints
ENDPOINT_CURRENT_PARAMETERS = "/0000/get_current_parameters"
ENDPOINT_TOTAL_ENERGY = "/0000/get_total_energy"

# Device types
DEVICE_TYPE_3PHASE = "3phase"
DEVICE_TYPE_1PHASE = "1phase"

# Sensor keys for 3-phase devices
SENSORS_3PHASE = {
    "energia_pobrana_l1": {
        "name": "Energy Import L1",
        "unit": "kWh",
        "device_class": "energy",
        "state_class": "total_increasing",
        "icon": "mdi:lightning-bolt",
    },
    "energia_pobrana_l2": {
        "name": "Energy Import L2",
        "unit": "kWh",
        "device_class": "energy",
        "state_class": "total_increasing",
        "icon": "mdi:lightning-bolt",
    },
    "energia_pobrana_l3": {
        "name": "Energy Import L3",
        "unit": "kWh",
        "device_class": "energy",
        "state_class": "total_increasing",
        "icon": "mdi:lightning-bolt",
    },
    "energia_pobrana_suma": {
        "name": "Energy Import Total",
        "unit": "kWh",
        "device_class": "energy",
        "state_class": "total_increasing",
        "icon": "mdi:lightning-bolt-circle",
    },
    "moc_czynna_l1": {
        "name": "Active Power L1",
        "unit": "W",
        "device_class": "power",
        "state_class": "measurement",
        "icon": "mdi:lightning-bolt",
    },
    "moc_czynna_l2": {
        "name": "Active Power L2",
        "unit": "W",
        "device_class": "power",
        "state_class": "measurement",
        "icon": "mdi:lightning-bolt",
    },
    "moc_czynna_l3": {
        "name": "Active Power L3",
        "unit": "W",
        "device_class": "power",
        "state_class": "measurement",
        "icon": "mdi:lightning-bolt",
    },
    "moc_czynna_suma": {
        "name": "Active Power Total",
        "unit": "W",
        "device_class": "power",
        "state_class": "measurement",
        "icon": "mdi:lightning-bolt-circle",
    },
    "natezenie_l1": {
        "name": "Current L1",
        "unit": "A",
        "device_class": "current",
        "state_class": "measurement",
        "icon": "mdi:current-ac",
    },
    "natezenie_l2": {
        "name": "Current L2",
        "unit": "A",
        "device_class": "current",
        "state_class": "measurement",
        "icon": "mdi:current-ac",
    },
    "natezenie_l3": {
        "name": "Current L3",
        "unit": "A",
        "device_class": "current",
        "state_class": "measurement",
        "icon": "mdi:current-ac",
    },
    "natezenie_suma": {
        "name": "Current Total",
        "unit": "A",
        "device_class": "current",
        "state_class": "measurement",
        "icon": "mdi:current-ac",
    },
    "napiecie_l1": {
        "name": "Voltage L1",
        "unit": "V",
        "device_class": "voltage",
        "state_class": "measurement",
        "icon": "mdi:sine-wave",
    },
    "napiecie_l2": {
        "name": "Voltage L2",
        "unit": "V",
        "device_class": "voltage",
        "state_class": "measurement",
        "icon": "mdi:sine-wave",
    },
    "napiecie_l3": {
        "name": "Voltage L3",
        "unit": "V",
        "device_class": "voltage",
        "state_class": "measurement",
        "icon": "mdi:sine-wave",
    },
    "moc_reaktywna_l1": {
        "name": "Reactive Power L1",
        "unit": "VAr",
        "device_class": None,
        "state_class": "measurement",
        "icon": "mdi:lightning-bolt",
    },
    "moc_reaktywna_l2": {
        "name": "Reactive Power L2",
        "unit": "VAr",
        "device_class": None,
        "state_class": "measurement",
        "icon": "mdi:lightning-bolt",
    },
    "moc_reaktywna_l3": {
        "name": "Reactive Power L3",
        "unit": "VAr",
        "device_class": None,
        "state_class": "measurement",
        "icon": "mdi:lightning-bolt",
    },
    "cos_phi_l1": {
        "name": "Power Factor L1",
        "unit": None,
        "device_class": None,
        "state_class": "measurement",
        "icon": "mdi:cosine-wave",
    },
    "cos_phi_l2": {
        "name": "Power Factor L2",
        "unit": None,
        "device_class": None,
        "state_class": "measurement",
        "icon": "mdi:cosine-wave",
    },
    "cos_phi_l3": {
        "name": "Power Factor L3",
        "unit": None,
        "device_class": None,
        "state_class": "measurement",
        "icon": "mdi:cosine-wave",
    },
    "czestotliwosc_l1": {
        "name": "Frequency L1",
        "unit": "Hz",
        "device_class": "frequency",
        "state_class": "measurement",
        "icon": "mdi:sine-wave",
    },
    "czestotliwosc_l2": {
        "name": "Frequency L2",
        "unit": "Hz",
        "device_class": "frequency",
        "state_class": "measurement",
        "icon": "mdi:sine-wave",
    },
    "czestotliwosc_l3": {
        "name": "Frequency L3",
        "unit": "Hz",
        "device_class": "frequency",
        "state_class": "measurement",
        "icon": "mdi:sine-wave",
    },
}

# Sensor keys for 1-phase devices
SENSORS_1PHASE = {
    "energia_pobrana": {
        "name": "Energy Import",
        "unit": "kWh",
        "device_class": "energy",
        "state_class": "total_increasing",
        "icon": "mdi:lightning-bolt",
    },
    "moc_czynna": {
        "name": "Active Power",
        "unit": "W",
        "device_class": "power",
        "state_class": "measurement",
        "icon": "mdi:lightning-bolt",
    },
    "natezenie": {
        "name": "Current",
        "unit": "A",
        "device_class": "current",
        "state_class": "measurement",
        "icon": "mdi:current-ac",
    },
    "napiecie": {
        "name": "Voltage",
        "unit": "V",
        "device_class": "voltage",
        "state_class": "measurement",
        "icon": "mdi:sine-wave",
    },
    "moc_reaktywna": {
        "name": "Reactive Power",
        "unit": "VAr",
        "device_class": None,
        "state_class": "measurement",
        "icon": "mdi:lightning-bolt",
    },
    "cos_phi": {
        "name": "Power Factor",
        "unit": None,
        "device_class": None,
        "state_class": "measurement",
        "icon": "mdi:cosine-wave",
    },
    "czestotliwosc": {
        "name": "Frequency",
        "unit": "Hz",
        "device_class": "frequency",
        "state_class": "measurement",
        "icon": "mdi:sine-wave",
    },
}

# Config flow
CONF_SCAN_INTERVAL = "scan_interval"

# Error messages
ERROR_CANNOT_CONNECT = "cannot_connect"
ERROR_INVALID_RESPONSE = "invalid_response"
