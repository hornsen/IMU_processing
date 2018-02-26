
# coding: utf-8

""" A script to process data generated from an IMU (MPU9250 Breakout) on a Arduino board """

# Import libaries
import os
import sys

import pandas as pd
import matplotlib.pyplot as plt
import tkinter.scrolledtext as tkst

from tkinter import *
from time import time

# Import Python files
sys.path.append('./Python_files/')
from calculations import *
from plot import *
from stopWatch import stopWatch


class IMU(Frame):
    def __init__(self,master):
        Frame.__init__(self, master)
        self.master = master
        
        # Initilize constants
        self.MEASUREMENT_FOLDER = './Measurement/'
        self.OUTPUT_PATH = './Output/'

        # List to keep track of setup configuration
        self.configuration=[]

        # Lists for the buttons
        self.buttonSensors = []
        self.buttonChoices = []

        # Names for all the lists
        self.SENSORS = ['ACC', 'GYR']
        self.CHOICES = ['CSV', 'Excel']

        # Dictionary for the lists
        self.dictionarySensors = {0:'ACC',1:'GYR'}
        self.dictionaryChoices = {0:'CSV',1:'Excel'}

        self.initUI()

    def initUI(self):
        # Title to the program
        self.master.title("IMU processing")

        # All the frames
        self.frameOne = Frame(self.master)
        self.frameOne.grid(row=1)
        self.frameTwo = Frame(self.master)
        self.frameTwo.grid(row=2)     
        self.frameThree = Frame(self.master)
        self.frameThree.grid(row=3)
        self.frameFour = Frame(self.master)
        self.frameFour.grid(row=4)
        self.frameFive = Frame(self.master)
        self.frameFive.grid(row=5)

        # IMU title
        Label(self.frameOne,text="IMU processing",width=25,font =('Arial',23)).grid()

        # Time labels
        labelCounter=1
        for label in ["Start time", "End time", "Frequency"]:
            Label(self.frameTwo,text=label,width=10,font =('Arial',15)).grid(row=0, column=labelCounter)
            labelCounter+=2

        # Entries   
        self.entryStartTime = Entry(self.frameTwo, width=10, font = ('Arial',15))
        self.entryStartTime.grid(row=0, column=2)   

        self.entryEndTime = Entry(self.frameTwo, width=10, font = ('Arial',15))
        self.entryEndTime.grid(row=0, column=4)

        self.entryFrequency = Entry(self.frameTwo, width=10, font = ('Arial',15))
        self.entryFrequency.grid(row=0, column=6)

        # ACC, GYR and MAG button
        sensorCounter = 0
        for sensor in self.SENSORS:
            self.buttonSensors.append(Button(self.frameThree, text=sensor, width = 10, relief='raised',
                        font = ('Arial',15), command=lambda num=sensorCounter: 
                                self.toggle(self.buttonSensors, self.dictionarySensors, num)))
            self.buttonSensors[sensorCounter].grid(row = 0, column=sensorCounter, pady=(10,10), padx=(10,0))
            sensorCounter += 1


        # CSV and Excel button
        choicesCounter = 0
        for choice in self.CHOICES:
            self.buttonChoices.append(Button(self.frameFour,text=choice, width=10,relief='raised',
                        font = ('Arial',15), command=lambda num=choicesCounter: 
                            self.toggle(self.buttonChoices, self.dictionaryChoices, num)))
            self.buttonChoices[choicesCounter].grid(row=0,column=choicesCounter,pady=(10,10),padx=(10,0))
            choicesCounter += 1


        # Start and quit button
        self.buttonStart = Button(self.frameFive, text="Start", width=10, font = ('Arial',15), 
                                                                                  command=self.processData)
        self.buttonStart.grid(row=0, column=1, pady=(10,10), padx=(10,0))

        self.buttonQuit = Button(self.frameFive, text="Quit", width=10, font = ('Arial',15), command=self.quit)
        self.buttonQuit.grid(row=0, column=2, pady=(10,10), padx=(10,0))

        self.buttonClear = Button(self.frameFive, text="Clear", width=10, font = ('Arial',15), command=self.clear)
        self.buttonClear.grid(row=0, column=3, pady=(10,10), padx=(10,0))

    def toggle(self, buttonList, buttonDictionary, buttonNum):
        # Makes the button stay pressed or open
        if(buttonList[buttonNum].config('relief')[-1] == 'sunken'):
            buttonList[buttonNum].config(relief='raised', background=root.cget("bg"))
            self.configuration.remove(buttonDictionary[buttonNum])
        else:
            buttonList[buttonNum].config(relief='sunken', background='lightgreen')
            self.configuration.append(buttonDictionary[buttonNum])

    def quit(self):
        # Close the script
        root.quit()

    def clear(self):
        # Clear all the input values and unlock buttons

        self.entryStartTime.delete(0, 'end')
        self.entryEndTime.delete(0, 'end')
        self.entryFrequency.delete(0, 'end')


        for buttons in self.buttonSensors, self.buttonChoices:
            for num in range(len(buttons)):
                buttons[num].config(relief='raised', background=root.cget("bg"))

    def numberCheck(self):
        # Function that check start time is less than end time and that they are ints
        if(self.entryStartTime.get()!=''):
            try: float(self.entryStartTime.get())
            except ValueError: self.txt.insert('end', 'Error! Start time needs to be a number')


        if(self.entryEndTime.get()!=''):
            try: float(self.entryEndTime.get())
            except ValueError: self.txt.insert('end', 'Error! End time needs to be a number')
                
    def measurementCheck(self):       
        # Create measurement folder if it doesn't exist
        if not os.path.exists(self.MEASUREMENT_FOLDER): os.makedirs(self.MEASUREMENT_FOLDER)
        
        # Load all measurement files
        self.allMeasurements = [f for f in os.listdir(self.MEASUREMENT_FOLDER) if f.endswith('.data')]
        
        # Print following message if there is no files in measurement folder
        if(len(self.allMeasurements)==0): 
            self.txt.insert('end', 'Please put all measurement measurements in folder "Measurement".') 
            
    def processData(self):
        # Initialize counter and timestamp
        startTime = time()

        # Starts the evalution of data
        self.scrollFrame = Frame(self.master)
        self.scrollFrame.grid(row=9, column=0)

        self.txt = tkst.ScrolledText(self.scrollFrame, font = ('Arial',13))
        self.txt.grid()

        self.numberCheck()
        self.measurementCheck()
        
        if(len(self.allMeasurements) > 0): 
            # Starting processing measurements
            self.txt.insert('end', "\n\n" + 86*"*" + "\n")
            self.txt.insert('end', '>>> STARTING PROCESSING IMU MEASUREMENTS <<<')
            self.txt.insert('end', '\n' + 86*"*" + '\n')

            self.main()

            self.txt.insert('end', "\n\n" + 86*"*" + "\n")
            self.txt.insert('end', '>>> PROCESSING IMU MEASUREMENTS COMPLETED <<<') 
            self.txt.insert('end', "\n" + 86*"*" + "\n\n")


            totalTime = time() - startTime
            self.txt.insert('end', '\n*** Total time processed: ' + stopWatch( totalTime ) + ' ***')

    def loadRawData(self):
        self.txt.insert('end', '\n\nPROCESSING MEASUREMENT %s OF %s: %s\n' % (self.measurementCounter,
                                                len(self.allMeasurements),self.measurement[:-14].upper()))
            
        self.txt.insert('end', 'Processing measurement: ' + self.measurement + '\n')
        self.txt.update_idletasks()
        self.dfRaw = pd.read_csv( os.path.join(self.MEASUREMENT_FOLDER, self.measurement), sep=' ', header = None)

        # Columns getting readable names
        self.dfRaw = self.dfRaw.rename(columns={0: 'Time', 1: 'Temperature',
                                    2: 'ACC X raw', 3: 'ACC Y raw', 4: 'ACC Z raw', 
                                    5: 'GYR X raw', 6: 'GYR Y raw', 7: 'GYR Z raw'
                                   })

    def changeFrequency(self):
        timeFrequency=self.dfRaw['Time'][::int(self.entryFrequency.get())].reset_index(drop=True)
        self.dfRaw=pd.merge(timeFrequency.to_frame(), self.dfRaw, how='inner')

    def accCalculations(self):
        self.txt.insert('end', 'Processing ACC\n')

        # ACC NORM
        accNormTemp = self.dfRaw.apply(calcAccNorm, axis=1)
        accNorm = pd.DataFrame(accNormTemp.tolist(), columns=('ACC norm', 'Time') )

        self.endResult = pd.merge(self.endResult, accNorm)

        plotAccData(self.measurement, self.endResult)

    def gyrCalculations(self):
        self.txt.insert('end', 'Processing GYR\n')
        
        # GYR angle in degree
        gyrAngle = calcGyrAngle( self.dfRaw )

        # Merge to earlier data frames
        self.endResult = pd.merge(self.endResult, gyrAngle)

        plotGyrData(self.measurement, self.endResult)
            
    def exportDataToCsv(self, measurement):
        self.txt.insert('end', '\nNext step: Export to CSV\n')
        self.txt.update_idletasks()
        csvProcessingTime = time()   

        # Export CSV file
        csvFileName=str(measurement[:-5])+".csv"
        self.endResult.to_csv( os.path.join(self.OUTPUT_PATH, csvFileName))

        self.txt.insert('end', 'Export to CSV completed '+stopWatch(time()-csvProcessingTime)+'\n')
        self.txt.update_idletasks()
        self.measurementTimer += time()-csvProcessingTime
    
    def exportDataToExcel(self, measurement):   
        self.txt.insert('end', '\nNext step: Export to Excel\n')
        self.txt.update_idletasks()
        excelProcessingTime= time()

        # Configure the output path and measurement name
        excelFileName=str(measurement[:-5])+'.xlsx'
        writer = pd.ExcelWriter(os.path.join(self.OUTPUT_PATH, excelFileName))
        self.endResult.to_excel(writer)
        writer.save()

        self.txt.insert('end', 'Export to Excel completed'
                                        +stopWatch(time()-excelProcessingTime)+'\n\n')
        self.txt.update_idletasks()
        self.measurementTimer += time()-excelProcessingTime


    def main(self):       
        # Reset variables
        self.measurementCounter = 0
        self.measurementTimer = 0
        
        # Lopp over all measurements
        for self.measurement in self.allMeasurements:
            # Reset Messung Timer
            preparationTimer=time()
            self.measurementCounter += 1          
            
            # Load raw data
            self.loadRawData() 
            
            # Shorten the time if requested
            if( self.entryStartTime.get() != ''): 
                self.dfRaw=self.dfRaw[self.dfRaw['Time']>= float(self.entryStartTime.get())]
            
            if( self.entryEndTime.get() != ''): 
                self.dfRaw=self.dfRaw[self.dfRaw['Time']<= float(self.entryEndTime.get()) ]
            
            # Frequency
            if(self.entryFrequency.get() != ''): self.changeFrequency()
            
            # Preperations complete
            self.measurementTimer+=time()-preparationTimer
            self.txt.insert('end', 'Preparation completed ' + stopWatch(time()-preparationTimer) +'\n\n') 
            self.txt.update_idletasks()  

            
            # Starting calculations
            self.txt.insert('end', 'Initialization: Calculation\n')
            self.txt.update_idletasks()
            calculationTime = time()
            self.endResult = self.dfRaw.copy()

            # Calculations
            if('ACC' in self.configuration): self.accCalculations()
            if('GYR' in self.configuration): self.gyrCalculations()

            # Calculations complete
            self.measurementTimer+=time()-calculationTime
            self.txt.insert('end', 'Calculation completed ' + stopWatch(time()-calculationTime) +'\n\n') 
            self.txt.update_idletasks()  
            
            
            # Export data to CSV and/or Excel
            if('CSV' in self.configuration): self.exportDataToCsv(self.measurement)
            if('Excel' in self.configuration): self.exportDataToExcel(self.measurement)

            # Print following when a measurement is done
            self.measurementTimerFinal = stopWatch(self.measurementTimer).upper()
            self.txt.insert('end', '\nPROCESSING MEASUREMENT: %s COMPLETED %s\n\n'%
                                                (self.measurement[:-14].upper(),self.measurementTimerFinal))

            self.txt.update_idletasks()


if __name__ == "__main__":
    root = Tk()
    IMU(root)

    root.mainloop()

