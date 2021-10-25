import covidmodule as cm
import matplotlib.pyplot as plt
from matplotlib.pyplot import figure
from matplotlib.animation import FuncAnimation
import numpy as np

figure(figsize=(8,8), dpi=100)

agents = []

#eigenschaften des Virus
covid19 = cm.virus(1.5, 14)

#initialisiere alle agenten
for i in range(10):
    for j in range(10):
        pos = cm.position(i,j)
        id = 10*i+1*j
        agent = cm.agent(id,pos,cm.agent.sir["s"],1,0.1)
        agents.append(agent)
        print(agent.SIRState)

#Wähle den ersten erkrankten aus
FIID = np.random.randint(0,100)
agents[FIID].SIRState=cm.agent.sir["i"]
firstill=agents[FIID]

#Größe der Marker
plt.plot(markersize=10)

#zeichne alle Agenten ein
for i in range(100):
    color="blue"
    if(agents[i].SIRState=="suspectible"):
        color="blue"
    elif(agents[i].SIRState=="infectious"):
        color="red"
    elif(agents[i].SIRState=="removed"):
        color="black"
    plt.scatter(agents[i].position.x, agents[i].position.y, c=color)

#infektionsradius
plt.scatter(firstill.position.x, firstill.position.y, s=covid19.infectionRadius*2*6000, c="red", alpha=0.3)

plt.xlabel("Position X")
plt.ylabel("Position Y")

plt.show()


