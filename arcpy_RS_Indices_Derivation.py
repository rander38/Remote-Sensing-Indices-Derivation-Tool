"""
Calculate spectral indices using satellite remote sensing data.

Author: Ryan S. Anderson
Email: RSAnderson@Protonmail.com

The MIT License (MIT)

Copyright (c) 2015 Ryan S. Anderson

Permission is hereby granted, free of charge, to any person obtaining a copy of
this software and associated documentation files (the "Software"), to deal in
the Software without restriction, including without limitation the rights to
use, copy, modify, merge, publish, distribute, sublicense, and to permit persons 
to whom the Software is furnished to do so, subject to the following conditions:

1.  You MAY NOT sell any application that you derive from the code in this repository 
without specific written permission from Ryan S. Anderson.

2.  The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software. 

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER
IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""

import os
import time
import ConfigParser
import Tkinter
import arcpy
from arcpy.sa import *
import arcgisscripting
from Tkinter import *
from ttk import Button
from tkFileDialog import askdirectory, askopenfilename

startTime = time.time()
gp = arcgisscripting.create(10.1)
arcpy.CheckOutExtension("spatial")
arcpy.env.overwriteOutput = 1

# Read .ini file
Config = ConfigParser.ConfigParser()
Config.read("Sensors_Formulas_RSIDT.ini")

# Set input stacked image and output directory if desired
inPath = r""
outPath = r""

# Get values from .ini file
indices = eval(Config.get("Parameters", "indices"))                 # List of indices
sensors = eval(Config.get("Parameters", "sensors"))                 # List of sensors
indicesSensor = eval(Config.get("Parameters", "indicesSensor"))     # Dictionary of indices with compatible sensors

# Set indices to disable based on sensor compatibility
MSS_Disable = []
TM_Disable = []
ETM_Disable = []
OLI_Disable = []
MODIS_Disable = []
WV_Disable = []
for key, value in indicesSensor.iteritems():
    if "Landsat 1-5 MSS" not in value:
        MSS_Disable.append(key)
    if "Landsat 4-5 TM" not in value:
        TM_Disable.append(key)
    if "Landsat 7 ETM+" not in value:
        ETM_Disable.append(key)
    if "Landsat 8 OLI" not in value:
        OLI_Disable.append(key)
    if "MODIS" not in value:
        MODIS_Disable.append(key)
    if "Worldview 02" not in value:
        WV_Disable.append(key)

# --------------Begin GUI----------------

top = Tk()
top.title("Remote Sensing Indices Derivation Tool")


def cbChecked():
    label['text'] = ''


# Set text to require reflectance or digital number based on sensor
def tcapshowstate(*args):
    if cbVar[indices.index("Brightness")].get() or cbVar[indices.index("Greenness")].get() or cbVar[indices.index("Wetness")].get():
        if vSensor.get() == "MODIS" or vSensor.get() == "Landsat 4-5 TM" or vSensor.get() == "Worldview 02" or vSensor.get() == "Landsat 7 ETM+" or vSensor.get() == "Landsat 8 OLI":
            form["text"] = "(Requires Reflectance)"
        if vSensor.get() == "Landsat 1-5 MSS": 
            form["text"] = "(Requires Digital Number (DN))"
    else:
        form["text"] = ""


def sectionBreak(index, title):
    if text == index:
        global rowpos, colpos
        colpos = 2
        rowpos += 1
        Label(top, text=title, font="Times 10").grid(row=rowpos,column=colpos, columnspan=3, sticky=W)
        rowpos += 1

exVar = IntVar()
ex = Checkbutton(top, text="Export Individual Bands", variable=exVar).grid(row=1, column=4, sticky=W, columnspan=2, padx=4, pady=4)

rowpos = 1
colpos = 2
cb = list(range(len(indices)))
cbVar = list(range(len(indices)))
for i, text in enumerate(indices):
    if colpos % 6 == 0:
        colpos = 2
        rowpos += 1
    sectionBreak("NDVI", "Vegetation Indices")
    sectionBreak("NDWI", "Hydrologic Indices")
    sectionBreak("Clay", "Geologic Indices")
    sectionBreak("NBR", "Burn Indices")
    sectionBreak("NDBI", "Miscellaneous Indices")
    if text == 'Brightness':
        colpos = 2
        rowpos += 1
        Label(top, text="Tasseled Cap Transformation", font="Times 10").grid(row=rowpos,column=colpos, columnspan=3, sticky=W)
        form = Label(top, text="", font="Times 10")
        form.grid(row=rowpos, column=4, columnspan=2, sticky=W)
        rowpos += 1
    cbVar[i] = IntVar()
    cb[i] = Checkbutton(top, text=text, variable=cbVar[i], command=cbChecked)
    cb[i].grid(row=rowpos, column=colpos, sticky=W, padx=4, pady=4)
    colpos += 1
label = Label(top, width=5)
label.grid(row=rowpos, column=colpos)
cbChecked()
rowpos += 1

# Set Labels
Label(top, text="Sensor", font="Times 12 bold").grid(row=1,column=1, sticky=W)
Label(top, text="Indices", font="Times 12 bold").grid(row=1,column=2, sticky=W)


# Set Radiobuttons
def rbChecked():
    label['text'] = ''

sensrowpos = 2
rb = list(range(len(sensors)))
vSensor = StringVar()
for i, sensor in enumerate(sensors):
    rb[i] = Radiobutton(top, text=sensor, variable=vSensor, value=sensor)
    rb[i].grid(row=sensrowpos, column=1, pady=4, padx=7, sticky=W)
    sensrowpos += 1
rbChecked()


def disable(sensor, disableList):
    if vSensor.get() == sensor:
        for i in indices:
            cbVar[indices.index(i)].set(1)
            cb[indices.index(i)].configure(state='normal')
        for i in disableList:
            cbVar[indices.index(i)].set(0)
            cb[indices.index(i)].configure(state='disabled')


# Disable or enable checkbuttons based on sensor selection
def showstate(*args):
    disable("Worldview 02", WV_Disable)
    disable("Landsat 4-5 TM", TM_Disable)
    disable("Landsat 7 ETM+", ETM_Disable)
    disable("Landsat 8 OLI", OLI_Disable)
    disable("MODIS", MODIS_Disable)
    disable("Landsat 1-5 MSS", MSS_Disable)

vSensor.trace_variable("w", showstate)
cbVar[indices.index("Brightness")].trace_variable("w", tcapshowstate)
cbVar[indices.index("Greenness")].trace_variable("w", tcapshowstate)
cbVar[indices.index("Wetness")].trace_variable("w", tcapshowstate)
vSensor.trace_variable("w", tcapshowstate)
vSensor.set("Landsat 4-5 TM")

top.resizable(0,0) # Disable window resizing

Label(top, text="Input Stacked Image").grid(row=rowpos,column=1, sticky=W)
rowpos += 1
indirVar = StringVar()
indirEntry = Entry(top, textvariable = indirVar, width=50)
indirEntry.delete(0, END)
indirEntry.insert(INSERT, inPath)
indirEntry.grid(row=rowpos,column=0, sticky=W, columnspan=8, padx=5)


def indirbrowser():
    indir = askopenfilename(parent=top, title="Select Stacked Input Image")
    if len(indir) > 0:
        indirEntry.delete(0, END)
        indirEntry.insert(INSERT, indir)

indirButton = Button(top, text = 'Browse', command=indirbrowser).grid(row=rowpos, column=4, pady=2, padx=2)
rowpos += 1

Label(top, text="Output Directory").grid(row=rowpos,column=1, sticky=W)
rowpos += 1
outdirVar = StringVar()
outdirEntry = Entry(top, textvariable = outdirVar, width=50)
outdirEntry.delete(0, END)
outdirEntry.insert(INSERT, outPath)
outdirEntry.grid(row=rowpos, column=1, sticky=W, columnspan=8, padx=5)


def outdirbrowser():
    outdir = askdirectory(parent=top, title="Select Root Output Directory", mustexist=1)
    if len(outdir) > 0:
        outdirEntry.delete(0, END)
        outdirEntry.insert(INSERT, outdir)

outdirButton = Button(top, text = 'Browse', command=outdirbrowser).grid(row=rowpos, column=4, pady=2, padx=2)
rowpos += 1


# Run Button
def callback():
    top.destroy()
Button(top, text = 'Run', command=callback).grid(row=rowpos,column=3, pady=4, padx=4)


# Quit Button
def quitbutton():
        print "Processing cancelled"
        top.destroy()
        raise SystemExit(0)
Button(top, text='Quit', command=quitbutton).grid(row=rowpos, column=2, pady=4, padx=4)    

top.mainloop()

# --------------End GUI----------------

# Set variables selected from GUI
Sensor = vSensor.get()
inPath = indirVar.get()
outPath = outdirVar.get()
arcpy.env.workspace = inPath

if not (outPath and os.path.exists(outPath)): os.makedirs(outPath)  # Create output directory if it doesn't exist
pathRoot, inRaster = os.path.split(inPath)
print "Processing", inRaster

d = arcpy.Describe(inPath)

# Set bands based on sensor
if Sensor == "Landsat 1-5 MSS":
    Green = Raster(d.children[0].name)
    Red = Raster(d.children[1].name)
    NIR1 = Raster(d.children[2].name)
    NIR2 = Raster(d.children[3].name)

if Sensor == "Landsat 4-5 TM" or Sensor == "Landsat 7 ETM+":
    Blue = Raster(d.children[0].name)
    Green = Raster(d.children[1].name)
    Red = Raster(d.children[2].name)
    NIR1 = Raster(d.children[3].name)
    SWIR1 = Raster(d.children[4].name)
    SWIR2 = Raster(d.children[5].name)

if Sensor == "Landsat 8 OLI":
    Coastal = Raster(d.children[0].name)
    Blue = Raster(d.children[1].name)
    Green = Raster(d.children[2].name)
    Red = Raster(d.children[3].name)
    NIR1 = Raster(d.children[4].name)
    SWIR1 = Raster(d.children[5].name)
    SWIR2 = Raster(d.children[6].name)

if Sensor == "MODIS":
    Red = Raster(d.children[0].name)
    NIR1 = Raster(d.children[1].name)
    Blue = Raster(d.children[2].name)
    Green = Raster(d.children[3].name)
    NIR2 = Raster(d.children[4].name)
    SWIR1 = Raster(d.children[5].name)
    SWIR2 = Raster(d.children[6].name)

if Sensor == "Worldview 02":
    Coastal = Raster(d.children[0].name)
    Blue = Raster(d.children[1].name)
    Green = Raster(d.children[2].name)
    Yellow = Raster(d.children[3].name)
    Red = Raster(d.children[4].name)
    RedEdge = Raster(d.children[5].name)
    NIR1 = Raster(d.children[6].name)
    NIR2 = Raster(d.children[7].name)

# Export individual Bands if selected
if exVar.get():
    bands = arcpy.ListRasters()
    print "Exporting Bands"
    for bandNo, bandName in enumerate(bands):
        outBand = Raster(bandName) * 1.0
        outBand.save(outPath + "/" + inRaster[:-4] + "_B" + str(bandNo + 1) + ".tif")

# Calculate and save indices
for key, value in indicesSensor.iteritems():
    if Sensor in value:
        if cbVar[indices.index(key)].get():  # Determine if indice was selected from GUI
            if key == 'Brightness' or key == 'Greenness' or key == 'Wetness' or key == 'Yellowness':  # Check if tasseled cap index
                formula = Config.get(Sensor, key)  # Get sensor specific tasseled cap coefficients
            else:
                formula = Config.get("Formulas", key)
            print key
            eval(formula).save(outPath + "/" + inRaster[:-4] + "_" + key + ".tif")  # Save index raster

endTime = time.time() - startTime
print "Completed in", ("%.2f" % endTime), 'seconds.'