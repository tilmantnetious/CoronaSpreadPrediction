import time

import numpy as np
import matplotlib.pyplot as plt

plt.style.use("seaborn-whitegrid")

#hier wird die Datei, die in main.py geneeriert wird, eingelesen. Einfach den array aus der Datei rauskopieren
#hier einfügen, und ganz am ende des arrays, das Komma löschen. Das ist dort zu viel. I know. ist unpraktikable, hatt für eine simple Auswertung aber gereicht



# erstelle 2 Plots
fig, (ax1, ax2, ax3, ax4) = plt.subplots(1, 4)

#Erfahre die Länge der längsten Liste
maxL = 0
for it in data:
    for types in it:
        if(len(types)>maxL):
            maxL=len(types)
print(maxL)

#x-Achse
timeList = np.linspace(0,400,num=maxL)

#Summe der Ausprägungen
lisd1, lisd2, lisd3, lisd4 = [],[],[],[]
while(maxL>len(lisd1)):
    lisd1.append(0)
    lisd2.append(0)
    lisd3.append(0)
    lisd4.append(0)

for it in data:
    for i in range(4):
        #Wenn 1. Array - sus
        if i==0:
            list1 = it[i].copy()
            while (maxL>len(list1)):
                list1.append(list1[-1])    
            for j in range(len(list1)):
                lisd1[j] += list1[j]     
            pl, = ax1.plot(timeList, list1, "blue", label="susceptible", alpha=0.03)
        #Wenn 2 Arrays - inf
        if i==1:
            list1 = it[i].copy()
            while (maxL>len(list1)):
                list1.append(list1[-1])
            for j in range(len(list1)):
                lisd2[j] += list1[j]     
            pl, = ax2.plot(timeList, list1, "red", label="infectious", alpha=0.03)
        #Wenn 3. Array - rem
        if i==2:
            list1 = it[i].copy()
            while (maxL>len(list1)):
                list1.append(list1[-1])
            for j in range(len(list1)):
                lisd3[j] += list1[j]     
            pl, = ax3.plot(timeList, list1, "green", label="recovered", alpha=0.03)
        #Wenn 4. Array - dead
        if i==3:
            list1 = it[i].copy()
            while (maxL>len(list1)):
                list1.append(list1[-1])
            for j in range(len(list1)):
                lisd4[j] += list1[j]     
            pl, = ax4.plot(timeList, list1, "grey", label="dead", alpha=0.03)

#Erwartungswert
for i in range(len(lisd1)):
    lisd1[i] = lisd1[i]/50
for i in range(len(lisd2)):
    lisd2[i] = lisd2[i]/50
for i in range(len(lisd3)):
    lisd3[i] = lisd3[i]/50
for i in range(len(lisd4)):
    lisd4[i] = lisd4[i]/50

list_sd1, list_sd2, list_sd3, list_sd4 = [],[],[],[]

while(maxL>len(list_sd1)):
    list_sd1.append(0)
    list_sd2.append(0)
    list_sd3.append(0)
    list_sd4.append(0)

#Standardabweichung
for it in data:
    for i in range(4):
        #Wenn 1. Array - sus
        if i==0:
            list1 = it[i].copy()
            while (maxL>len(list1)):
                list1.append(list1[-1])   
            for j in range(len(list1)):
                list_sd1[j]+=(list1[j]-list_sd1[j])^2
#            pl, = ax1.plot(timeList, list1, "blue", label="susceptible", alpha=0.25)
        #Wenn 2 Arrays - inf
        if i==1:
            list1 = it[i].copy()
            while (maxL>len(list1)):
                list1.append(list1[-1])
            for j in range(len(list1)):
                list_sd2[j]+=(list1[j]-list_sd2[j])^2
#            pl, = ax2.plot(timeList, list1, "red", label="infectious", alpha=0.25)
        #Wenn 3. Array - rem
        if i==2:
            list1 = it[i].copy()
            while (maxL>len(list1)):
                list1.append(list1[-1])
            for j in range(len(list1)):
                list_sd3[j]+=(list1[j]-list_sd3[j])^2   
#            pl, = ax3.plot(timeList, list1, "green", label="recovered", alpha=0.25)
        #Wenn 4. Array - dead
        if i==3:
            list1 = it[i].copy()
            while (maxL>len(list1)):
                list1.append(list1[-1])
            for j in range(len(list1)):
                list_sd4[j]+=(list1[j]-list_sd4[j])^2
#            pl, = ax4.plot(timeList, list1, "grey", label="dead", alpha=0.25)

#Standardabweichung
for i in range(len(lisd1)):
    list_sd1[i] = list_sd1[i]/49
for i in range(len(lisd2)):
    list_sd2[i] = list_sd2[i]/49
for i in range(len(lisd3)):
    list_sd3[i] = list_sd3[i]/49
for i in range(len(lisd4)):
    list_sd4[i] = list_sd4[i]/49

list1plus = lisd1.copy()
list2plus = lisd2.copy()
list3plus = lisd3.copy()
list4plus = lisd4.copy()
list1minus = lisd1.copy()
list2minus = lisd2.copy()
list3minus = lisd3.copy()
list4minus = lisd4.copy()

for i in range(len(lisd1)):
    list1plus[i] = list1plus[i]+list_sd1[i]
    list1minus[i] = list1minus[i]-list_sd1[i]
for i in range(len(lisd2)):
    list2plus[i] = list2plus[i]+list_sd2[i]
    list2minus[i] = list2minus[i]-list_sd2[i]
for i in range(len(lisd3)):
    list3plus[i] = list3plus[i]+list_sd3[i]
    list3minus[i] = list3minus[i]-list_sd3[i]
for i in range(len(lisd4)):
    list4plus[i] = list4plus[i]+list_sd4[i]
    list4minus[i] = list4minus[i]-list_sd4[i]


ple, = ax1.plot(timeList, list1plus,"blue")
plf, = ax2.plot(timeList, list2plus,"red")
plg, = ax3.plot(timeList, list3plus,"green")
plh, = ax4.plot(timeList, list4plus,"grey")

pli, = ax1.plot(timeList, list1minus,"blue")
plj, = ax2.plot(timeList, list2minus,"red")
plk, = ax3.plot(timeList, list3minus,"green")
pll, = ax4.plot(timeList, list4minus,"grey")


pla, = ax1.plot(timeList, lisd1,"black")
plb, = ax2.plot(timeList, lisd2,"black")
plc, = ax3.plot(timeList, lisd3,"black")
pld, = ax4.plot(timeList, lisd4,"black")

print(lisd1[-1])
print(lisd2[-1])
print(lisd3[-1])
print(lisd4[-1])
print(list_sd1[-1])
print(list_sd2[-1])
print(list_sd3[-1])
print(list_sd4[-1])


ax1.set_title("Infectious")
ax1.set_xlabel("Time")
ax1.set_ylabel("Agents")

ax2.set_title("Infectious")
ax2.set_xlabel("Time")

ax3.set_title("Recovered")
ax3.set_xlabel("Time")

ax4.set_title("Dead")
ax4.set_xlabel("Time")


#NICHT VERGESSEN, die Achsen anzupassen falls ontwendig
ax1.set_xlim(0, 400)
ax1.set_ylim(0, 100)

ax2.set_xlim(0, 400)
ax2.set_ylim(0, 100)
ax3.set_xlim(0, 400)
ax3.set_ylim(0, 100)
ax4.set_xlim(0, 400)
ax4.set_ylim(0, 100)

fig.suptitle("SuperBasisKonfiguration")

print()

plt.show()

