"""
Ruleset. Calculates and returns a Ruleset for Simulation

@author David Hammbartsumjan
@author Tilman Schlichting
@since 27.10.2021
@copyright CC BY-SA
"""
import json
from collections import namedtuple

def jsonDecode(dictionary):
    """
    Wrapper that creates an Object from Dictionary
    :param dictionary: Configuration from JSON-File
    :return: object: Configuration as Object
    """
    return namedtuple('X', dictionary.keys(), )(*dictionary.values())

class Ruleset:
    def __init__(self, file):
        self.config = json.load(file, object_hook=jsonDecode)
