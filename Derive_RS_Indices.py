'''
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
'''

import arcpy, Tkinter, os, time
from arcpy.sa import *
import arcgisscripting
from Tkinter import *
from ttk import Button
from tkFileDialog import askdirectory, askopenfilename

startTime = time.time()
gp = arcgisscripting.create(10.1)
arcpy.CheckOutExtension("spatial")
arcpy.env.overwriteOutput = 1

## Set input stacked image and output directory
inPath = ""
outPath = ""

## Create output directory if it doesn't exist
if not os.path.exists(outPath): os.makedirs(outPath)

indices = [
'NDVI',
'NDMI',
'NDSI',
'NDWI',
'MNDWI',
'SAVI',
'MSAVI2',
'NBR',
'NMDI',
'NHFD',
'Brightness',
'Greenness',
'Wetness',
'Yellowness'
]

MSS_Disable = [
'NDSI',
'NHFD',
'NDMI',
'MNDWI',
'NBR',
'NMDI',
'Wetness'
]

TM_ETM_OLI_MODIS_Disable = [
'NDSI',
'NHFD',
'Yellowness'
]

WV_Disable = [
'NDMI',
'MNDWI',
'NBR',
'NMDI',
'Yellowness'
]

## GUI
top = Tk()
top.title("Process Imagery")

def cbChecked():
    label['text'] = ''

rowpos = 2
colpos = 2    
cb = list(range(len(indices)))
cbVar = list(range(len(indices)))
for i, text in enumerate(indices):
    if colpos % 6 == 0:
        colpos = 2
        rowpos += 1
    cbVar[i] = Tkinter.IntVar()
    cb[i] = Tkinter.Checkbutton(top, text=text,
        variable=cbVar[i], command=cbChecked)
    cb[i].grid(row=rowpos, column=colpos, sticky=W, padx=4, pady=4)
    colpos += 1
    cbVar[i].set(1)
label = Tkinter.Label(top, width=5)
label.grid(row=rowpos, column=colpos)
cbChecked()

# Set Labels
Label(top, text="Sensor", font="Times 12 bold").grid(row=1,column=1, sticky=W)
Label(top, text="Indices", font="Times 12 bold").grid(row=1,column=2, sticky=W)
Label(top, text="Input Stacked Image").grid(row=8,column=1, sticky=W)
Label(top, text="Output Directory").grid(row=10,column=1, sticky=W)

# Set Radiobuttons
vSensor = StringVar()
cTMETM = Radiobutton(top, text= "Landsat 1-3 MSS", variable = vSensor, value = "MSS").grid(row=2, column=1, pady=4, padx=4, sticky=W)
cTMETM = Radiobutton(top, text= "Landsat 4-5 TM", variable = vSensor, value = "TM").grid(row=3, column=1, pady=4, padx=4, sticky=W)
cTMETM = Radiobutton(top, text= "Landsat 7 ETM+", variable = vSensor, value = "ETM").grid(row=4, column=1, pady=4, padx=4, sticky=W)
cOLI = Radiobutton(top, text= "Landsat 8 OLI", variable = vSensor, value = "OLI").grid(row=5, column=1, pady=4, padx=4, sticky=W)
cMODIS = Radiobutton(top, text= "MODIS", variable = vSensor, value = "MODIS").grid(row=6, column=1, pady=4, padx=4, sticky=W)
cWV = Radiobutton(top, text= "Worldview 02", variable = vSensor, value = "WV").grid(row=7, column=1, pady=4, padx=4, sticky=W)

def showstate(*args):
    if vSensor.get() == "WV":
        for i in indices:
            cbVar[indices.index(i)].set(1)
            cb[indices.index(i)].configure(state='normal')
        for i in WV_Disable:
            cbVar[indices.index(i)].set(0)
            cb[indices.index(i)].configure(state='disabled')
    elif vSensor.get() == 'TM' or vSensor.get() == 'ETM' or vSensor.get() == 'MODIS' or vSensor.get() == 'OLI':
        for i in indices:
            cbVar[indices.index(i)].set(1)
            cb[indices.index(i)].configure(state='normal')
        for i in TM_ETM_OLI_MODIS_Disable:
            cbVar[indices.index(i)].set(0)
            cb[indices.index(i)].configure(state='disabled')
    elif vSensor.get() == 'MSS':
        for i in WV_Disable:
            cbVar[indices.index(i)].set(1)
            cb[indices.index(i)].configure(state='normal')
        for i in MSS_Disable:
            cbVar[indices.index(i)].set(0)
            cb[indices.index(i)].configure(state='disabled')

def tcapshowstate(*args):
    if cbVar[indices.index("Brightness")].get() or cbVar[indices.index("Greenness")].get() or cbVar[indices.index("Wetness")].get():
        if vSensor.get() == "MODIS" or vSensor.get() == "TM" or vSensor.get() == "WV" or vSensor.get() == "ETM" or vSensor.get() == "OLI":
            form["text"] = "Tasseled Cap Transformation for \n" + vSensor.get() + " requires Reflectance"
        if vSensor.get() == "MSS": 
            form["text"] = "Tasseled Cap Transformation for \n" + vSensor.get() + " requires Digital Number (DN)"
    else:
        form["text"] = ""

form = Label(top, text="", font=("arial 9"))
form.grid(row=6, column=2, columnspan=4, rowspan=2, sticky=N)

vSensor.trace_variable("w", showstate)
cbVar[indices.index("Brightness")].trace_variable("w", tcapshowstate)
cbVar[indices.index("Greenness")].trace_variable("w", tcapshowstate)
cbVar[indices.index("Wetness")].trace_variable("w", tcapshowstate)
vSensor.trace_variable("w", tcapshowstate)
vSensor.set("TM")

top.resizable(0,0) # Disable window resizing

indirVar = StringVar()
indirEntry = Entry(top, textvariable = indirVar, width=50)
indirEntry.delete(0, END)
indirEntry.insert(INSERT, inPath)
indirEntry.grid(row=9,column=0, sticky=W, columnspan=8, padx=5)

def indirbrowser():
    indir1 = askopenfilename(parent=top, title="Select Stacked Input Image")
    if len(indir1) > 0:
        indirEntry.delete(0, END)
        indirEntry.insert(INSERT, indir1)

indirButton = Button(top, text = 'Browse', command=indirbrowser).grid(row=9, column=5, pady=2, padx=2)

outdirVar = StringVar()
outdirEntry = Entry(top, textvariable = outdirVar, width=50)
outdirEntry.delete(0, END)
outdirEntry.insert(INSERT, outPath)
outdirEntry.grid(row=11, column=1, sticky=W, columnspan=8, padx=5)

def outdirbrowser():
    outdir1 = askdirectory(parent=top, title="Select Root Output Directory", mustexist=1)
    if len(outdir1) > 0:
        outdirEntry.delete(0, END)
        outdirEntry.insert(INSERT, outdir1)

outdirButton = Button(top, text = 'Browse', command=outdirbrowser).grid(row=11, column=5, pady=2, padx=2)

## Run Button
def callback():
    top.destroy()
Button(top, text = 'Run', command=callback).grid(row=12,column=2, pady=4, padx=4)

## Quit Button
def quitbutton():
        print "Processing cancelled"
        top.destroy()
        raise SystemExit(0)

Button(top, text='Quit', command=quitbutton).grid(row=12, column=3, pady=4, padx=4)    

top.mainloop()

## Set variables from GUI
Sensor = vSensor.get()
inPath = indirVar.get()
outPath = outdirVar.get()

arcpy.env.workspace = inPath

inPath, inRaster = os.path.split(inPath)
print "Processing", inRaster

bands = arcpy.ListRasters()

## Set band values
if Sensor == "MSS":
    BlueBand = "1"
    GreenBand = "2"
    RedBand = "3"
    NIR1Band = "4"

if Sensor == "TM" or Sensor == "ETM":
    BlueBand = "1"
    GreenBand = "2"
    RedBand = "3"
    NIR1Band = "4"
    SWIR1Band = "5"
    SWIR2Band = "6"

if Sensor == "OLI":
    CoastalBand = "1"
    BlueBand = "2"
    GreenBand = "3"
    RedBand = "4"
    NIR1Band = "5"
    SWIR1Band = "6"
    SWIR2Band = "7"
    CirrusBand = "9"

if Sensor == "MODIS":
    RedBand = "1"
    NIR1Band = "2"
    BlueBand = "3"
    GreenBand = "4"
    NIR2Band = "5"
    SWIR1Band = "6"
    SWIR2Band = "7"

if Sensor == "WV":
    CoastalBand = "1"
    BlueBand = "2"
    GreenBand = "3"
    YellowBand = "4"
    RedBand = "5"
    RedEdgeBand = "6"
    NIR1Band = "7"
    NIR2Band = "8"

## Export individual bands
band = 0
if exportIndBands == 1:
    for bandfile in bands:
        band += 1
        outBand = Raster(bandfile) * 1.0
        outBand.save(outPath + "/" + inRaster[:-4] + "_B" + str(band) + ".tif")

## Set band files based on sensor
Green = Raster(outPath + "/"  + inRaster[:-4] + "_B" + GreenBand + ".tif")
Red = Raster(outPath + "/"  + inRaster[:-4] + "_B" + RedBand + ".tif")
NIR1 = Raster(outPath + "/"  + inRaster[:-4] + "_B" + NIR1Band + ".tif")
Blue = Raster(outPath + "/"  + inRaster[:-4] + "_B" + BlueBand + ".tif")

if Sensor == "WV" or Sensor == "OLI":
    Coastal = Raster(outPath + "/" + inRaster[:-4] + "_B" + CoastalBand + ".tif")

if Sensor == "WV":
    Yellow = Raster(outPath + "/"  + inRaster[:-4] + "_B" + YellowBand + ".tif")
    RedEdge = Raster(outPath + "/"  + inRaster[:-4] + "_B" + RedEdgeBand + ".tif")

if Sensor == "WV" or Sensor == "MODIS":
    NIR2 = Raster(outPath + "/"  + inRaster[:-4] + "_B" + NIR2Band + ".tif")

if Sensor == "TM" or Sensor == "ETM" or Sensor == "OLI" or Sensor == "MODIS":
    SWIR1 = Raster(outPath + "/"  + inRaster[:-4] + "_B" + SWIR1Band + ".tif")
    SWIR2 = Raster(outPath + "/"  + inRaster[:-4] + "_B" + SWIR2Band + ".tif")

if Sensor == "MSS":
    indicesForm = {
        'NDVI':(NIR1 - Red)/(NIR1 + Red),
        'NDWI':(Green - NIR1)/(Green + NIR1),
        'SAVI':((NIR1 - Red)/(NIR1 + Red + 0.5)) * (1 + 0.5),
        'MSAVI2':(2 * NIR1 + 1 - SquareRoot((2 * NIR1 + 1)**2 - 8 * (NIR1-Red)))/2,
        }

## Select which possible indices to calculate based on sensor
if Sensor == "TM" or Sensor == "ETM" or Sensor == "OLI" or Sensor == "MODIS":
    indicesForm = {
        'NDVI':(NIR1 - Red)/(NIR1 + Red),
        'NDMI':(NIR1 - SWIR1)/(NIR1 + SWIR1),
        'NDWI':(Green - NIR1)/(Green + NIR1),
        'MNDWI':(Green - SWIR1)/(Green + SWIR1),
        'SAVI':((NIR1 - Red)/(NIR1 + Red + 0.5)) * (1 + 0.5),
        'MSAVI2':(2 * NIR1 + 1 - SquareRoot((2 * NIR1 + 1)**2 - 8 * (NIR1-Red)))/2,
        'NBR':(NIR1 - SWIR1)/(NIR1 - SWIR1),
        'NMDI':(NIR1 - (SWIR1 - SWIR2))/(NIR1 + (SWIR1 - SWIR2))
        }

if Sensor == "WV":
    indicesForm = {
        'NDVI':(NIR1 - Red)/(NIR1 + Red),
        'NDSI':(Green - Yellow)/(Green + Yellow),
        'NDWI':(Green - NIR1)/(Green + NIR1),
        'SAVI':((NIR1 - Red)/(NIR1 + Red + 0.5)) * (1 + 0.5),
        'MSAVI2':(2 * NIR1 + 1 - SquareRoot((2 * NIR1 + 1)**2 - 8 * (NIR1 - Red)))/2,
        'NHFD':(RedEdge - Coastal)/(RedEdge + Coastal)
        }

## Add Tasseled Cap Transformation with sensor specific coefficients
if Sensor == "MSS": 
    indicesForm['Brightness'] = (Blue * 0.433) + (Green * 0.632) + (Red * 0.586) + (NIR1 * 0.264)
    indicesForm['Greenness'] = (Blue * -0.290) + (Green * -0.562) + (Red * 0.600) + (NIR1 * 0.491)
    indicesForm['Yellowness'] = (Blue * -0.829) + (Green * 0.522) + (Red * -0.039) + (NIR1 * 0.194)

''' MSS Requires Digital Number (DN)
Kauth, R., & Thomas, G. (1976). The tasselled cap--a graphic description of the spectral-temporal development of agricultural crops
as seen by Landsat. LARS Symposia.
'''

if Sensor == "OLI": 
    indicesForm['Brightness'] = (Blue * 0.3029) + (Green * 0.2786) + (Red * 0.4733) + (NIR1 * 0.5599) + (SWIR1 * 0.508) + (SWIR2 * 0.1872)
    indicesForm['Greenness'] = (Blue * -0.2941) + (Green * -0.243) + (Red * -0.5424) + (NIR1 * 0.7276) + (SWIR1 * 0.0713) + (SWIR2 * -0.1608)
    indicesForm['Wetness'] = (Blue * 0.1511) + (Green * 0.1973) + (Red * 0.3283) + (NIR1 * 0.3407) + (SWIR1 * -0.7117) + (SWIR2 * -0.4559)

''' Requires at-satellite reflectance
Coefficients derived from:
Baig, M. H. A., Zhang, L., Shuai, T., & Tong, Q. (2015). Derivation of a tasselled cap transformation based on Landsat 8 at-satellite reflectance.
Remote Sensing Letters, 5(5), 423-431. doi:10.1080/2150704X.915434
'''

if Sensor == "TM":
    indicesForm['Brightness'] = (Blue * 0.2043) + (Green * 0.4158) + (Red * 0.5524) + (NIR1 * 0.5741) + (SWIR1 * 0.3124) + (SWIR2 * 0.2303)
    indicesForm['Greenness'] = (Blue * -0.1603) + (Green * -0.2819) + (Red * -0.4934) + (NIR1 * 0.7940) + (SWIR1 * 0.0002) + (SWIR2 * -0.1446)
    indicesForm['Wetness'] = (Blue * 0.0315) + (Green * 0.2021) + (Red * 0.3102) + (NIR1 * 0.1594) + (SWIR1 * -0.6806) + (SWIR2 * -0.6109)

''' Requires surface reflectance
Coefficients derived from:
Crist, E. P. (1985). A TM Tasseled Cap equivalent transformation for reflectance factor data. Remote Sensing of Environment, 17(3), 301-306. doi:10.1016/0034-4257(85)90102-6
  '''    

if Sensor == "ETM":
    indicesForm['Greenness'] = (Blue * -0.3344) + (Green * -0.3544) + (Red * -0.4556) + (NIR1 * 0.6966) + (SWIR1 * -0.0242) + (SWIR2 * -0.2630)
    indicesForm['Brightness'] = (Blue * 0.3561) + (Green * 0.3972) + (Red * 0.3904) + (NIR1 * 0.6966) + (SWIR1 * 0.2286) + (SWIR2 * 0.1596)
    indicesForm['Wetness'] = (Blue * 0.2626) + (Green * 0.2141) + (Red * 0.0926) + (NIR1 * 0.0656) + (SWIR1 * -0.7629) + (SWIR2 * -0.5388)

''' Requires at-satellite reflectance
Coefficients derived from:
Huang, C., Wylie, B., Yang, L., Homer, C., & Zylstra, G. (2002). Derivation of a tasselled cap transformation based on Landsat 7 at-satellite reflectance.
International Journal of Remote Sensing, 23(8), 1741-1748. doi:10.1080/01431160110106113
'''

if Sensor == "MODIS":
    indicesForm['Brightness'] = (Blue * 0.3354) + (Green * 0.3834) + (Red * 0.3956) + (NIR1 * 0.4718) + (NIR2 * 0.3946) + (SWIR1 * 0.3434) + (SWIR2 * 0.2964)
    indicesForm['Greenness'] = (Blue * -0.2129) + (Green * -0.2222) + (Red * -0.3399) + (NIR1 * 0.5952) + (NIR2 * 0.4617) + (SWIR1 * -0.1037) + (SWIR2 * -0.4600)
    indicesForm['Wetness'] = (Blue * 0.5065) + (Green * 0.4040) + (Red * 0.10839) + (NIR1 * 0.0912) + (NIR2 * -0.2410) + (SWIR1 * -0.4658) + (SWIR2 * -0.5306)

''' Requires surface reflectance
Coefficients derived from:
    Zhang, X. Z. X., Schaaf, C. B., Friedl, M. a., Strahler, a. H., Gao, F. G. F., & Hodges, J. C. F. (2002). 
MODIS tasseled cap transformation and its utility. IEEE International Geoscience and Remote Sensing Symposium, 
2(C), 1063-1065. doi:10.1109/IGARSS.2002.1025776
  '''

if Sensor == "WV":
    indicesForm['Brightness'] = (Coastal * -0.060436) + (Blue * 0.012147) + (Green *  0.125846) + (Yellow * 0.313039) + (Red *  0.412175) + (RedEdge * 0.482758) + (NIR1 * -0.160654) + (NIR2 * 0.673510)
    indicesForm['Greenness'] = (Coastal * -0.140191) + (Blue * -0.206224) + (Green * -0.215854) + (Yellow * -0.314441) + (Red * -0.410892) + (RedEdge * 0.095786) + (NIR1 * 0.600549) + (NIR2 * 0.503672)
    indicesForm['Wetness'] = (Coastal * -0.270951) + (Blue * -0.315708) + (Green * -0.317263) + (Yellow * -0.242544) + (Red * -0.256463) + (RedEdge * -0.096550) + (NIR1 * -0.742535) + (NIR2 * 0.202430)
    
''' Requires surface reflectance
Coefficients derived from:
    Yarbough, L. D., Navulur, K., & Ravi, R. (2014). Presentation of the Kauth-Thomas transform for Worldview-2 reflectance data.
Remote Sensing Letters, 5(2), 131-138. doi:10.1080/2150704X.2014.885148
  '''

def CalculateIndice(text, indice):
    if cbVar[indices.index(text)].get():
        print text
        indice.save(outPath + "/" + inRaster[:-4] + "_" + text + ".tif")

for key,value in indicesForm.iteritems():
    CalculateIndice(key,value)
    
endTime = time.time() - startTime
print "Completed in", ("%.2f" % endTime), 'seconds.'
