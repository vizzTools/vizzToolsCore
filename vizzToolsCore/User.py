""" User configuration """

from .Models import *
from .Serialization import *
import json

def load_config(config_path=".vtc_config.json"):
    try:
        config = open(config_path, 'r')
    except:
        print(f"VTC config not found at {config_path}")
    return config


def add_sd_publisher():
