"""
Configurable logging package with modern standards and customizability

Developed by Coggl, and you 💖
Licensed under MIT, Coggl 2023
"""
import yaml
from datetime import datetime

#* Preload configuration file
with open("payload.yaml", "r") as stream:
    try:
        config = (yaml.safe_load(stream))
    except yaml.YAMLError as exc:
        print(exc)
    except FileNotFoundError:
        print("Create 'payload.yaml' in the root directory")

#* Load all YAML configuration
THEME = config.get('theme')
PAYLOAD = config.get('payload')
PAYLOAD_EXT = config.get('payload-extensions')

#* Create TYPE identifier for log level
def DEBUG():
    return 'DEBUG'

def INFO():
    return 'INFO'

def WARNING():
    return 'WARNING'

def ERROR():
    return 'ERROR'

def CRITICAL():
    return 'CRITICAL'

#? To be updated
#* Quick code configuration
def settings(loglevel: object = DEBUG):
    LEVELS = [DEBUG, INFO, WARNING, ERROR, CRITICAL]
    if loglevel in LEVELS:
        log_num = (LEVELS.index(loglevel))
        

class log():
    """
    Log a developer event using configuration from 'payload.yaml'
    """

    file = PAYLOAD.get('log')

    def debug():
        with open(log.file, "w") as f:
            f.write('DEBUG')
    
    def info():
        pass

    def warning():
        pass

    def error():
        pass

    def critical():
        pass
