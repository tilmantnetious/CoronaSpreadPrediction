"""
Corona Spread Prediction

@author David Hammbartsumjan
@author Tilman Schlichting
@since 27.10.2021
@copyright CC BY-SA

"""
from ruleset import ruleset
from simulation import sim

class Main:
    def __init__(self):
        """Konstruktor"""
        self.config = open('config.json')


# Intitialize runtime
runtime = Main()

# Create a ruleset with Paramenters from JSON
runtime.ruleset = ruleset.Ruleset(runtime.config).getRuleset()

#Create a Simulation with given Rulesets
runtime.sim = sim.Sim(runtime.ruleset)

#Debugpoint
print("hold")