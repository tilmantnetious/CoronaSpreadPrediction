"""
Virus. Contains Parameters describing the Covid Virus

@author David Hammbartsumjan
@author Tilman Schlichting
@since 27.10.2021
@copyright CC BY-SA
"""

class Virus:
    def __init__(self, conf):
        self.virus = conf

    def getVirus(self):
        return self.virus