"""
Animation- Class
Handles the Animation of passed
Data-Arrays from the Simulation

@author David Hammbartsumjan
@author Tilman Schlichting
@since 23.11.2021
@copyright CC BY-SA

"""

import matplotlib.pyplot as plt
import matplotlib.animation
import numpy as np


class Animation:
    def __init__(self, settings, result):

        self.settings = settings
        self.extingtDisease = False
        self.animation = False
        self.duration = 100
        self.step = 0

        #Settings from Simulation
        self.start_x_pos = result['frame']['x_pos'][0]
        self.start_y_pos = result['frame']['y_pos'][0]
        self.start_color = result['frame']['color'][0]
        self.x_lim = result['frame']['x_lim']
        self.y_lim = result['frame']['y_lim']
        self.env_name = result['frame']['env_name']
        self.pop_amount = result['frame']['pop_amount']

        self.SusAmmountList = result['movement']['SusAmmountList']
        self.InfAmmountList = result['movement']['InfAmmountList']
        self.RemAmmountList = result['movement']['RemAmmountList']
        self.TimeList = result['movement']['timeList']
        self.colorList = result['movement']['colorList']
        self.x_pos = result['frame']['x_pos']
        self.y_pos = result['frame']['y_pos']



    def __initFrame(self):

        # erstelle 2 Plots
        fig, (ax1, ax2) = plt.subplots(1, 2)

        # Scatter Plot - Simulation
        sc = ax1.scatter(self.start_x_pos, self.start_y_pos, color=self.start_color)

        #initiolisierung des Line-Plots
        pl1, = ax2.plot([], [], "-b", label="susceptible")
        pl2, = ax2.plot([], [], "-r", label="infectious")
        pl3, = ax2.plot([], [], "-g", label="removed")
        ax2.legend(loc="upper left")

        # Scatter Plot Spezifikationen
        ax1.set_xlim(0, self.x_lim)
        ax1.set_ylim(0, self.y_lim)
        ax1.set_xlabel("Position X")
        ax1.set_ylabel("Position Y")
        ax1.set_title(str(self.env_name) + " Simulation")

        # Line Plot Spezifikationen
        ax2.set_ylim(0, self.pop_amount)
        ax2.set_xlabel("Time")
        ax2.set_ylabel("Agents")
        ax2.set_title(str(self.env_name) + " Spread")

        return fig, pl1, pl2, pl3, sc


    def __callback_animation(self,fig, pl1, pl2, pl3, sc, printToFile = False):
        # Update die Daten der Simualtion (Koordinaten der Agenten)
        sc.set_offsets(np.c_[self.x_pos[self.step +1], self.y_pos[self.step +1]])
        sc.set_facecolor(self.colorList[self.step +1])

        # Update die Daten der Verbreitung (Kennzahlen der Gruppen)
        pl1.set_data(self.TimeList[self.step], self.SusAmmountList[self.step])
        pl2.set_data(self.TimeList[self.step], self.InfAmmountList[self.step])
        pl3.set_data(self.TimeList[self.step], self.RemAmmountList[self.step])
        # Update die x Achse des Line Plots
        fig.ax2.relim()
        fig.ax2.autoscale_view()

        #Stepping
        self.step += 1

    def animate(self):

        """
        Animates the given Dataset
        :return:
        """
        fig, pl1, pl2, pl3, sc = self.__initFrame()


        self.animation = matplotlib.FuncAnimation(fig
                                                  , self.__callback_animation(fig, pl1, pl2, pl3, sc, printToFile=False)
                                                  , frames = self.settings.framesPerSecond * self.duration
                                                  , interval = self.settings.intervalPerFrame
                                                  , repeat=self.extingtDisease)
        plt.show()