"""
Corona Spread Prediction

@author David Hammbartsumjan
@author Tilman Schlichting
@since 27.10.2021
@copyright CC BY-SA

"""
from ruleset import ruleset
from simulation import sim
from out import animation

class Main:
    def __init__(self):
        """Konstruktor"""
        self.config = open('CoronaSpreadPrediction\\config.json')


# Intitialize runtime
runtime = Main()
user_defined = ruleset.Ruleset(runtime.config)

# Create a ruleset with Paramenters from JSON
runtime.ruleset = user_defined.getRuleset()

allsim = "["
for i in range(50):
    print(i)
    allsim += "["
    #Create a Simulation with given Rulesets
    runtime.sim = sim.Sim(runtime.ruleset)

    #setStopCondition(duration -int =Dauer der Simulation in Sekunden, extinctDiseas -Bool =standardmäßig False, wenn true,
    # hört die Simulation auf, wenn die Krankheit ausgestorben ist)
    # @todo --> JSON - parameter
    # @todo --> StopCondition raushauen
    runtime.sim.setStopCondition(duration=300)

    result = runtime.sim.start(25)
    r = open("SuperBasisKonfiguration_result3.txt","a")
    allsim+=("[")
    for el in result["movement"]["SusAmmountList"][-1]:
        allsim += str(el)+","
    allsim = allsim[:-1]
    allsim+=("],[")
    for el in result["movement"]["InfAmmountList"][-1]:
        allsim+=str(el)+","
    allsim = allsim[:-1]
    allsim+=("],[")
    for el in result["movement"]["RemAmmountList"][-1]:
        allsim+=str(el)+","
    allsim = allsim[:-1]
    allsim+=("],[")
    for el in result["movement"]["DeaAmmountList"][-1]:
        allsim+=(str(el)+",")
    allsim = allsim[:-1]
    allsim+=("]],")
allsim+="]"
r.write(allsim)
print("done")

#create Simulation
#settings = user_defined.getSettings()
#runtime.animation = animation.Animation(settings, result).show()
