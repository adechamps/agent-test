"""Graphical user interface file of the project"""

import Tkinter as tk
import tkSimpleDialog
import tkMessageBox
import tkFileDialog
import subprocess
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import sys
from agent import *
from importer import *
from simulate import *
from agents_memory import *


class GUIApp:

    def __init__(self,master):
        """GUIApp constructor, initializes the fisrt values."""
        self.agents = []
        self.master = master
        self.master.title("AgentTest")
        self.nbYearsSimulated = 0
        self.nbYearsToSimulate = 0
        self.speedTab = [0.1,0.2,0.5,1,2,5,10]
        self.simulSpeed = 1
        self.Brand_Factor = 0    #must be between 0.1 and 2.9 once entered
        self.count = self.countOutput()
        self.drawWidgets()
        self.drawBarChartBreed()
        self.drawBarChartStatus()
        self.drawLineChartBreed()
        self.memory = AgentsMemory() #stores the simulation state for each year
        self.askBrand_Factor()

    def drawWidgets(self):
        """Draw menu bar, text, buttons..."""
        #MENU#
        menubar = tk.Menu(self.master)
        filemenu = tk.Menu(menubar, tearoff=0)
        filemenu.add_command(label="New", command=self.newWindow)
        filemenu.add_command(label="Import dataset", command=self.importDataset)
        filemenu.add_command(label="Export dataset", command=self.exportDataSet)
        filemenu.add_command(label="Close", command=self.onClose)
        filemenu.add_separator()
        filemenu.add_command(label="Exit", command=self.onExit)
        menubar.add_cascade(label="File", menu=filemenu)
        configmenu = tk.Menu(menubar, tearoff=0)
        configmenu.add_command(label="Change Brand_Factor", command=self.changeBrand_Factor)
        menubar.add_cascade(label="Config", menu=configmenu)

        self.master.config(menu=menubar)
        ######

        #COUNTING#
        self.nbAgentsLabel = tk.Label(self.master, text="0 agents")
        self.nbAgentsLabel.grid(row=0,column=0, sticky=tk.W)
        self.nbBreed_CLabel = tk.Label(self.master, text="Breed_C : 0")
        self.nbBreed_CLabel.grid(row=1,column=0, sticky=tk.W)
        self.nbBreed_NCLabel = tk.Label(self.master, text="Breed_NC : 0")
        self.nbBreed_NCLabel.grid(row=2,column=0, sticky=tk.W)
        self.nbBreed_CLostLabel = tk.Label(self.master, text="Breed_C Lost : 0")
        self.nbBreed_CLostLabel.grid(row=3,column=0, sticky=tk.W)
        self.nbBreed_CGainedLabel = tk.Label(self.master, text="Breed_C Gained : 0")
        self.nbBreed_CGainedLabel.grid(row=4,column=0, sticky=tk.W)
        self.nbBreed_CRegainedLabel = tk.Label(self.master, text="Breed_C Regained : 0")
        self.nbBreed_CRegainedLabel.grid(row=5,column=0, sticky=tk.W)
        self.nbUnchangedLabel = tk.Label(self.master, text="Unchanged : 0")
        self.nbUnchangedLabel.grid(row=6,column=0, sticky=tk.W)
        ######

        #SIMULATE#
        self.Brand_FactorLabel = tk.Label(self.master, text="Brand_Factor : "+str(self.Brand_Factor))
        self.Brand_FactorLabel.grid(row=0, column=1, columnspan=3)
        self.nbYearsEntry = tk.Entry(self.master)
        self.nbYearsEntry.insert(tk.END,"15")
        self.nbYearsEntry.config(width=6, justify='right')
        self.nbYearsEntry.grid(row=1, column=1, columnspan=2, sticky=tk.E)
        yearsLabel = tk.Label(self.master, text="years")
        yearsLabel.grid(row=1, column=3, sticky=tk.W)
        yearsLabel.config(justify='left')
        decreaseSpeedButton = tk.Button(self.master, text=" - ", command=self.decreaseSpeed)
        decreaseSpeedButton.grid(row=2,column=1)
        self.speedLabel = tk.Label(self.master, text="Speed x1")
        self.speedLabel.grid(row=2,column=2)
        increaseSpeedButton = tk.Button(self.master, text=" + ", command=self.increaseSpeed)
        increaseSpeedButton.grid(row=2,column=3)
        simulButton = tk.Button(self.master, text="Launch simulation !", command=self.launchSimul)
        simulButton.grid(row=3,column=1, columnspan=3)
        stopSimulButton = tk.Button(self.master, text="Stop", command=self.stopSimul)
        stopSimulButton.grid(row=4,column=1, columnspan=3)
        self.nbYearsSimulatedLabel = tk.Label(self.master, text="Year : 0")
        self.nbYearsSimulatedLabel.grid(row=5,column=1, rowspan=2, columnspan=3)
        ######

    def drawBarChartBreed(self):
        """Draw the bar chart showing the number of agents in each breed"""
        self.figBarChartBreed = Figure(figsize=(3, 2), dpi=100)
        self.axBarChartBreed = self.figBarChartBreed.add_subplot(111)
        width=0.4
        self.axBarChartBreed.bar([0.5,1.5], [self.count["nbBreed_C"], self.count["nbBreed_NC"]], bottom=0, width=width)
        self.axBarChartBreed.set_xticks(np.arange(2) + 0.5 + width/2)
        self.axBarChartBreed.set_xticklabels(["Breed_C","Breed_NC"])
        self.figBarChartBreed.tight_layout()
        self.graphBarChartBreed = FigureCanvasTkAgg(self.figBarChartBreed, master=self.master)
        canvasBarChartBreed = self.graphBarChartBreed.get_tk_widget()
        canvasBarChartBreed.grid(row=7, column=0, columnspan=4)

    def updateBarChartBreed(self):
        """Update the bar chart breed."""
        self.axBarChartBreed.clear()
        width=0.4
        self.axBarChartBreed.bar([0.5,1.5], [self.count["nbBreed_C"], self.count["nbBreed_NC"]], bottom=0, width=width)
        self.axBarChartBreed.set_xticks(np.arange(2) + 0.5 + width/2)
        self.axBarChartBreed.set_xticklabels(["Breed_C","Breed_NC"])
        self.figBarChartBreed.tight_layout()
        self.graphBarChartBreed.draw()

    def drawBarChartStatus(self):
        """Draw the bar chart showing the number of agents with each status"""
        self.figBarChartStatus = Figure(figsize=(6, 2), dpi=100)
        self.axBarChartStatus = self.figBarChartStatus.add_subplot(111)
        width=0.4
        self.axBarChartStatus.bar([0.5,1.5, 2.5, 3.5], [self.count["nbLost"], self.count["nbGained"], self.count["nbRegained"], self.count["nbUnchanged"]], bottom=0, width=width)
        self.axBarChartStatus.set_xticks(np.arange(4) + 0.5 + width/2)
        self.axBarChartStatus.set_xticklabels(["Breed_C Lost","Breed_C Gained", "Breed_C Regained", "Unchanged"])
        self.figBarChartStatus.tight_layout()
        self.graphBarChartStatus = FigureCanvasTkAgg(self.figBarChartStatus, master=self.master)
        canvas = self.graphBarChartStatus.get_tk_widget()
        canvas.grid(row=7, column=4)

    def updateBarChartStatus(self):
        """Update the bar chart status."""
        self.axBarChartStatus.clear()
        width=0.4
        self.axBarChartStatus.bar([0.5,1.5, 2.5, 3.5], [self.count["nbLost"], self.count["nbGained"], self.count["nbRegained"], self.count["nbUnchanged"]], bottom=0, width=width)
        self.axBarChartStatus.set_xticks(np.arange(4) + 0.5 + width/2)
        self.axBarChartStatus.set_xticklabels(["Breed_C Lost","Breed_C Gained", "Breed_C Regained", "Unchanged"])
        self.figBarChartStatus.tight_layout()
        self.graphBarChartStatus.draw()

    def drawLineChartBreed(self):
        """Draw the line chart showing the number of agents in each breed during the 10 last years simulated"""
        x , y1, y2 = self.getLineChartBreedValues()
        self.figLineChartBreed = Figure(figsize=(12, 2), dpi=112)
        self.ax1LineChartBreed = self.figLineChartBreed.add_subplot(121)
        self.ax2LineChartBreed = self.figLineChartBreed.add_subplot(122)
        self.ax1LineChartBreed.set_xlabel('Year')
        self.ax2LineChartBreed.set_xlabel('Year')
        self.ax1LineChartBreed.set_ylabel('Breed_C', color='g')
        self.ax2LineChartBreed.set_ylabel('Breed_NC', color='r')
        self.figLineChartBreed.tight_layout()
        self.ax1LineChartBreed.plot(x, y1, 'g-o')
        self.ax2LineChartBreed.plot(x, y2, 'r-o')
        self.graphLineChartBreed = FigureCanvasTkAgg(self.figLineChartBreed, master=self.master)
        canvas = self.graphLineChartBreed.get_tk_widget()
        canvas.grid(row=8, column=0, columnspan=8)

    def updateLineChartBreed(self):
        """Update the line chart breed."""
        x , y1, y2 = self.getLineChartBreedValues()
        self.ax1LineChartBreed.clear()
        self.ax2LineChartBreed.clear()
        self.ax1LineChartBreed.set_xlabel('Year')
        self.ax2LineChartBreed.set_xlabel('Year')
        self.ax1LineChartBreed.set_ylabel('Breed_C', color='g')
        self.ax2LineChartBreed.set_ylabel('Breed_NC', color='r')
        self.figLineChartBreed.tight_layout()
        self.ax1LineChartBreed.plot(x, y1, 'g-o')
        self.ax2LineChartBreed.plot(x, y2, 'r-o')
        self.graphLineChartBreed.draw()

    def getLineChartBreedValues(self):
        """Returns the line chart breed values : number of agents in each breed in the last 10 years."""
        x = [self.nbYearsSimulated]
        y1 = [self.count["nbBreed_C"]]
        y2 = [self.count["nbBreed_NC"]]
        if self.nbYearsSimulated > 0:
            max=0
            l = reversed(list(enumerate(self.memory.count)))
            for i,e in l:
                x.insert(0, i)
                y1.insert(0, e["nbBreed_C"])
                y2.insert(0, e["nbBreed_NC"])
                max+=1
                if max==9:
                    break
        return x, y1, y2


    def askBrand_Factor(self):
        """Asks the Brand_Factor value while the input is not correct."""
        while self.Brand_Factor<0.1 or self.Brand_Factor>2.9:
            inpt = tkSimpleDialog.askfloat("Brand_Factor needed","Please enter Brand Factor (range 0.1 -> 2.9) : ")
            try:
                self.Brand_Factor = float(inpt)
            except:
                pass
        self.refreshDisplay()

    def changeBrand_Factor(self):
        """Modifies the Brand_Factor value."""
        self.Brand_Factor = 0
        self.askBrand_Factor()

    def onExit(self):
        """Destroys the current window."""
        if tkMessageBox.askyesno("Confirm", "Are you sure you want to exit ?"):
            self.master.destroy()

    def onClose(self):
        """Closes the current simulation. Reset the data."""
        if tkMessageBox.askyesno("Confirm", "Are you sure you want to close current simulation ?"):
            self.resetData()
            self.refreshDisplay()

    def importDataset(self):
        """Opens a window to choose a csv file to input data."""
        opts = {}
        opts['filetypes'] = [('CSV files','.csv'),('all files','.*')]
        filename = tkFileDialog.askopenfilename(**opts)
        if filename:
            try:
                self.resetData()
                self.agents = importData(filename)
            except Exception as e:
                tkMessageBox.showerror("Error", "Importation failed : "+str(e))
            finally:
                self.refreshDisplay()

    def exportDataSet(self):
        """Choose where to save current dataset"""
        opts = {}
        opts['filetypes'] = [('CSV files','.csv'),('all files','.*')]
        filename = tkFileDialog.asksaveasfilename(**opts)
        if filename:
            try:
                exportData(filename, self.agents)
            except Exception as e:
                tkMessageBox.showerror("Error", "Exportation failed : "+str(e))

    def resetData(self):
        """Resets all the data to default value."""
        self.agents = []
        self.nbYearsSimulated = 0
        self.nbYearsToSimulate = 0
        self.simulSpeed = 1
        self.memory = AgentsMemory()

    def eraseDisplay(self):
        """Erases the display."""
        if self.nbAgentsLabel:
            self.nbAgentsLabel.destroy()
        if self.nbBreed_CLabel:
            self.nbBreed_CLabel.destroy()
        if self.nbBreed_NCLabel:
            self.nbBreed_NCLabel.destroy()
        if self.nbBreed_CLostLabel:
            self.nbBreed_CLostLabel.destroy()
        if self.nbBreed_CGainedLabel:
            self.nbBreed_CGainedLabel.destroy()
        if self.nbBreed_CRegainedLabel:
            self.nbBreed_CRegainedLabel.destroy()
        if self.nbUnchangedLabel:
            self.nbUnchangedLabel.destroy()
        if self.nbYearsSimulatedLabel:
            self.nbYearsSimulatedLabel.destroy()
        if self.Brand_FactorLabel:
            self.Brand_FactorLabel.destroy()

    def refreshDisplay(self):
        """Refresh displayed values."""
        self.count = self.countOutput()
        #COUNTING#
        self.nbAgentsLabel.config(text=str(len(self.agents))+" agents")
        self.nbBreed_CLabel.config(text="Breed_C : "+str(self.count["nbBreed_C"]))
        self.nbBreed_NCLabel.config(text="Breed_NC : "+str(self.count["nbBreed_NC"]))
        self.nbBreed_CLostLabel.config(text="Breed_C Lost : "+str(self.count["nbLost"]))
        self.nbBreed_CGainedLabel.config(text="Breed_C Gained : "+str(self.count["nbGained"]))
        self.nbBreed_CRegainedLabel.config(text="Breed_C Regained : "+str(self.count["nbRegained"]))
        self.nbUnchangedLabel.config(text="Unchanged : "+str(self.count["nbUnchanged"]))
        ######

        #SIMULATE#
        self.Brand_FactorLabel.config(text="Brand_Factor : "+str(self.Brand_Factor))
        self.speedLabel.config(text="Speed x"+str(self.simulSpeed))
        self.nbYearsSimulatedLabel.config(text="Year : "+str(self.nbYearsSimulated))
        ######

        #CHARTS#
        self.updateBarChartBreed()
        self.updateBarChartStatus()
        self.updateLineChartBreed()
        ########

        self.master.update_idletasks() #forcing the update

    def countOutput(self):
        """Function counting the number of agent with each breed and status."""
        nbBreed_C=0
        nbBreed_NC=0
        nbLost=0
        nbGained=0
        nbRegained=0
        nbUnchanged=0
        for agent in self.agents:
            if agent.Agent_Breed == "Breed_C":
                nbBreed_C+=1
            elif agent.Agent_Breed == "Breed_NC":
                nbBreed_NC+=1
            if agent.Breed_Actual_Status == "Breed_C Lost":
                nbLost+=1
            elif agent.Breed_Actual_Status == "Breed_C Gained":
                nbGained+=1
            elif agent.Breed_Actual_Status == "Breed_C Regained":
                nbRegained+=1
            elif agent.Breed_Actual_Status == "Unchanged":
                nbUnchanged+=1
        return {"nbBreed_C":nbBreed_C,"nbBreed_NC":nbBreed_NC,"nbLost":nbLost, "nbGained":nbGained, "nbRegained":nbRegained, "nbUnchanged":nbUnchanged}

    def launchSimul(self):
        """Launching simulation."""
        try:
            nbYears = int(self.nbYearsEntry.get())
        except:
            tkMessageBox.showerror("Error", "This is not an integer !")
        else:
            if nbYears > 0:
                self.nbYearsToSimulate = nbYears
                self.simul()


    def simul(self):
        """Simulate during self.nbYearsToSimulate years."""
        if self.nbYearsToSimulate > 0:
            self.memory.saveState(self.agents, self.Brand_Factor, self.count) #save the current state before next state
            simulate1year(self.agents, self.Brand_Factor)
            self.nbYearsSimulated+=1
            self.nbYearsToSimulate-=1
            self.nbYearsEntry.delete(0, 'end')
            self.nbYearsEntry.insert(tk.END,str(self.nbYearsToSimulate))
            self.refreshDisplay()
            delay = int(1000 / self.simulSpeed)
            self.master.after(delay, self.simul)

    def stopSimul(self):
        """Stop current simulation."""
        self.nbYearsToSimulate = 0

    def decreaseSpeed(self):
        """Decreases the simulation speed."""
        i = self.speedTab.index(self.simulSpeed)
        if i > 0:
            self.simulSpeed = self.speedTab[i-1]
            self.refreshDisplay()

    def increaseSpeed(self):
        """Increases the simulation speed."""
        i = self.speedTab.index(self.simulSpeed)
        if i < (len(self.speedTab)-1):
            self.simulSpeed = self.speedTab[i+1]
            self.refreshDisplay()

    def newWindow(self):
        """Opens a new window independent from the current window."""
        subprocess.Popen([sys.executable,"main.py"])
        

     
