"""
Environment.

@author David Hammbartsumjan
@author Tilman Schlichting
@since 27.10.2021
@copyright CC BY-SA
"""

class Environment:
    def __init__(self, conf):
        self.env = conf

    def getEnvironment(self):
        return self.env