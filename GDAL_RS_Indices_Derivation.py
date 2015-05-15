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

import Tkinter, os, time, numpy
from gdal_calculations import *
from Tkinter import *
from ttk import Button
from tkFileDialog import askdirectory, askopenfilename

startTime = time.time()

Env.overwrite = True

## Set input stacked image and output directory if desired
inPath = r""
outPath = r""

indices = [
## Vegetatoion
'NDVI',
'SAVI',
'MSAVI2',
'EVI',
'EVI2',
'NDMI',
'NMDI',
## Hydrologic
'NDWI',
'MNDWI',
## Geologic
'Clay',
'Ferrous',
'Iron Oxide',
'WVII',
'WVSI',
# Burn
'NBR',
'BAI',
## Miscellaneous
'NDBI',
'NHFD',
'NDSI',
## Tasseled Cap
'Brightness',
'Greenness',
'Wetness',
'Yellowness',
]

MSS_Disable = [
'NHFD',
'NDMI',
'MNDWI',
'NBR',
'NMDI',
'Wetness',
'Clay',
'Ferrous',
'WVII',
'WVSI',
'NDBI'
]

TM_ETM_OLI_MODIS_Disable = [
'NHFD',
'Yellowness',
'WVII',
'WVSI',
]

WV_Disable = [
'NDMI',
'MNDWI',
'NBR',
'NMDI',
'Yellowness',
'Clay',
'Ferrous',
'NDBI'
]

sensors = [
"Landsat 1-5 MSS",
"Landsat 4-5 TM",
"Landsat 7 ETM+",
"Landsat 8 OLI",
"MODIS",
"Worldview 02"
]

## GUI
top = Tk()
top.title("Remote Sensing Indices Derivation Tool")

def cbChecked():
    label['text'] = ''

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
#    cbVar[i].set(1)
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
    
## Disable or enable checkbuttons based on sensor selection
def showstate(*args):
    disable("Worldview 02", WV_Disable)
    disable("Landsat 4-5 TM", TM_ETM_OLI_MODIS_Disable)
    disable("Landsat 7 ETM+", TM_ETM_OLI_MODIS_Disable)
    disable("Landsat 8 OLI", TM_ETM_OLI_MODIS_Disable)
    disable("MODIS", TM_ETM_OLI_MODIS_Disable)
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

## Run Button
def callback():
    top.destroy()
Button(top, text = 'Run', command=callback).grid(row=rowpos,column=3, pady=4, padx=4)

## Quit Button
def quitbutton():
        print "Processing cancelled"
        top.destroy()
        raise SystemExit(0)
Button(top, text='Quit', command=quitbutton).grid(row=rowpos, column=2, pady=4, padx=4)    

top.mainloop()

## Set variables from GUI
Sensor = vSensor.get()
inPath = indirVar.get()
outPath = outdirVar.get()

## Create output directory if it doesn't exist
if not (outPath and os.path.exists(outPath)): os.makedirs(outPath)

inP, inRasterStr = os.path.split(inPath)
print "Processing", inRasterStr

inRaster = Dataset(inPath)

## Set band values
if Sensor == "Landsat 1-5 MSS":
    Blue = Float32(inRaster.get_raster_band(1))
    Green = Float32(inRaster.get_raster_band(2))
    Red = Float32(inRaster.get_raster_band(3))
    NIR1 = Float32(inRaster.get_raster_band(4))

if Sensor == "Landsat 4-5 TM" or Sensor == "Landsat 7 ETM+":
    Blue = Float32(inRaster.get_raster_band(1))
    Green = Float32(inRaster.get_raster_band(2))
    Red = Float32(inRaster.get_raster_band(3))
    NIR1 = Float32(inRaster.get_raster_band(4))
    SWIR1 = Float32(inRaster.get_raster_band(5))
    SWIR2 = Float32(inRaster.get_raster_band(6))

if Sensor == "Landsat 8 OLI":
    Coastal = Float32(inRaster.get_raster_band(1))
    Blue = Float32(inRaster.get_raster_band(2))
    Green = Float32(inRaster.get_raster_band(3))
    Red = Float32(inRaster.get_raster_band(4))
    NIR1 = Float32(inRaster.get_raster_band(5))
    SWIR1 = Float32(inRaster.get_raster_band(6))
    SWIR2 = Float32(inRaster.get_raster_band(7))
    Cirrus = Float32(inRaster.get_raster_band(9))

if Sensor == "MODIS":
    Red = Float32(inRaster.get_raster_band(1))
    NIR1 = Float32(inRaster.get_raster_band(2))
    Blue = Float32(inRaster.get_raster_band(3))
    Green = Float32(inRaster.get_raster_band(4))
    NIR2 = Float32(inRaster.get_raster_band(5))
    SWIR1 = Float32(inRaster.get_raster_band(6))
    SWIR2 = Float32(inRaster.get_raster_band(7))

if Sensor == "Worldview 02":
    Coastal = Float32(inRaster.get_raster_band(1))
    Blue = Float32(inRaster.get_raster_band(2))
    Green = Float32(inRaster.get_raster_band(3))
    Yellow = Float32(inRaster.get_raster_band(4))
    Red = Float32(inRaster.get_raster_band(5))
    RedEdge = Float32(inRaster.get_raster_band(6))
    NIR1 = Float32(inRaster.get_raster_band(7))
    NIR2 = Float32(inRaster.get_raster_band(8))

# Export individual Bands
if exVar.get():
    print "Exporting Bands"
    for bandNo in range(inRaster._nbands):
        outBand = inRaster.get_raster_band(bandNo + 1) * 1.0
        outBand.save(outPath + "/" + inRasterStr[:-4] + "_B" + str(bandNo + 1) + ".tif")

# Set indice equations compatible with all sensors
print "Calculating Indices"
indicesForm = {
    'NDVI':(NIR1 - Red)/(NIR1 + Red),
    'EVI':2.5*((NIR1 - Red)/(NIR1 + 6 * Red - 7.5 * Blue + 1)),
    'EVI2':2.4*((NIR1 - Red)/(NIR1 + Red + 1)),
    'NDWI':(Green - NIR1)/(Green + NIR1),
    'SAVI':((NIR1 - Red)/(NIR1 + Red + 0.5)) * (1 + 0.5),
    'MSAVI2':(2 * NIR1 + 1 - numpy.sqrt((2 * NIR1 + 1)**2 - 8 * (NIR1-Red)))/2,
    'Iron Oxide':(Red/Blue),
    'BAI':1/((0.1-Red)**2 + (0.06 - NIR1)**2),
    'NDSI':(Green - NIR1)/(Green + NIR1)
    }

## Add sensor specific indices
if Sensor == "Landsat 4-5 TM" or Sensor == "Landsat 7 ETM+" or Sensor == "Landsat 8 OLI" or Sensor == "MODIS":
    indicesForm['NDMI'] = (NIR1 - SWIR1)/(NIR1 + SWIR1)
    indicesForm['MNDWI'] = (Green - SWIR1)/(Green + SWIR1)
    indicesForm['NBR'] = (NIR1 - SWIR1)/(NIR1 + SWIR1)
    indicesForm['NMDI'] = (NIR1 - (SWIR1 - SWIR2))/(NIR1 + (SWIR1 - SWIR2))
    indicesForm['Clay'] = (SWIR1/SWIR2)
    indicesForm['Ferrous'] = (SWIR1/NIR1)
    indicesForm['NDBI'] = (SWIR1 - NIR1)/(SWIR1 + NIR1)

## Add Tasseled Cap Transformation with sensor specific coefficients
if Sensor == "Landsat 1-5 MSS": 
    indicesForm['Brightness'] = (Blue * 0.433) + (Green * 0.632) + (Red * 0.586) + (NIR1 * 0.264)
    indicesForm['Greenness'] = (Blue * -0.290) + (Green * -0.562) + (Red * 0.600) + (NIR1 * 0.491)
    indicesForm['Yellowness'] = (Blue * -0.829) + (Green * 0.522) + (Red * -0.039) + (NIR1 * 0.194)

''' Requires Digital Number (DN)
Kauth, R., & Thomas, G. (1976). The tasselled cap--a graphic description of the spectral-temporal development of agricultural crops
as seen by Landsat. LARS Symposia.
'''

if Sensor == "Landsat 8 OLI": 
    indicesForm['Brightness'] = (Blue * 0.3029) + (Green * 0.2786) + (Red * 0.4733) + (NIR1 * 0.5599) + (SWIR1 * 0.508) + (SWIR2 * 0.1872)
    indicesForm['Greenness'] = (Blue * -0.2941) + (Green * -0.243) + (Red * -0.5424) + (NIR1 * 0.7276) + (SWIR1 * 0.0713) + (SWIR2 * -0.1608)
    indicesForm['Wetness'] = (Blue * 0.1511) + (Green * 0.1973) + (Red * 0.3283) + (NIR1 * 0.3407) + (SWIR1 * -0.7117) + (SWIR2 * -0.4559)

''' Requires Reflectance
Baig, M. H. A., Zhang, L., Shuai, T., & Tong, Q. (2015). Derivation of a tasselled cap transformation based on Landsat 8 at-satellite reflectance.
Remote Sensing Letters, 5(5), 423-431. doi:10.1080/2150704X.915434
'''

if Sensor == "Landsat 4-5 TM":
    indicesForm['Brightness'] = (Blue * 0.2043) + (Green * 0.4158) + (Red * 0.5524) + (NIR1 * 0.5741) + (SWIR1 * 0.3124) + (SWIR2 * 0.2303)
    indicesForm['Greenness'] = (Blue * -0.1603) + (Green * -0.2819) + (Red * -0.4934) + (NIR1 * 0.7940) + (SWIR1 * 0.0002) + (SWIR2 * -0.1446)
    indicesForm['Wetness'] = (Blue * 0.0315) + (Green * 0.2021) + (Red * 0.3102) + (NIR1 * 0.1594) + (SWIR1 * -0.6806) + (SWIR2 * -0.6109)

''' Requires Reflectance
Crist, E. P. (1985). A TM Tasseled Cap equivalent transformation for reflectance factor data. Remote Sensing of Environment, 17(3), 301-306. doi:10.1016/0034-4257(85)90102-6
'''    

if Sensor == "Landsat 7 ETM+":
    indicesForm['Greenness'] = (Blue * -0.3344) + (Green * -0.3544) + (Red * -0.4556) + (NIR1 * 0.6966) + (SWIR1 * -0.0242) + (SWIR2 * -0.2630)
    indicesForm['Brightness'] = (Blue * 0.3561) + (Green * 0.3972) + (Red * 0.3904) + (NIR1 * 0.6966) + (SWIR1 * 0.2286) + (SWIR2 * 0.1596)
    indicesForm['Wetness'] = (Blue * 0.2626) + (Green * 0.2141) + (Red * 0.0926) + (NIR1 * 0.0656) + (SWIR1 * -0.7629) + (SWIR2 * -0.5388)

''' Requires Reflectance
Huang, C., Wylie, B., Yang, L., Homer, C., & Zylstra, G. (2002). Derivation of a tasselled cap transformation based on Landsat 7 at-satellite reflectance.
International Journal of Remote Sensing, 23(8), 1741-1748. doi:10.1080/01431160110106113
'''

if Sensor == "MODIS":
    indicesForm['Brightness'] = (Blue * 0.3354) + (Green * 0.3834) + (Red * 0.3956) + (NIR1 * 0.4718) + (NIR2 * 0.3946) + (SWIR1 * 0.3434) + (SWIR2 * 0.2964)
    indicesForm['Greenness'] = (Blue * -0.2129) + (Green * -0.2222) + (Red * -0.3399) + (NIR1 * 0.5952) + (NIR2 * 0.4617) + (SWIR1 * -0.1037) + (SWIR2 * -0.4600)
    indicesForm['Wetness'] = (Blue * 0.5065) + (Green * 0.4040) + (Red * 0.10839) + (NIR1 * 0.0912) + (NIR2 * -0.2410) + (SWIR1 * -0.4658) + (SWIR2 * -0.5306)

''' Requires Reflectance
    Zhang, X. Z. X., Schaaf, C. B., Friedl, M. a., Strahler, a. H., Gao, F. G. F., & Hodges, J. C. F. (2002). 
MODIS tasseled cap transformation and its utility. IEEE International Geoscience and Remote Sensing Symposium, 
2(C), 1063-1065. doi:10.1109/IGARSS.2002.1025776
'''

if Sensor == "Worldview 02":
    indicesForm['NHFD'] = (RedEdge - Coastal)/(RedEdge + Coastal)
    indicesForm['Brightness'] = (Coastal * -0.060436) + (Blue * 0.012147) + (Green *  0.125846) + (Yellow * 0.313039) + (Red *  0.412175) + (RedEdge * 0.482758) + (NIR1 * -0.160654) + (NIR2 * 0.673510)
    indicesForm['Greenness'] = (Coastal * -0.140191) + (Blue * -0.206224) + (Green * -0.215854) + (Yellow * -0.314441) + (Red * -0.410892) + (RedEdge * 0.095786) + (NIR1 * 0.600549) + (NIR2 * 0.503672)
    indicesForm['Wetness'] = (Coastal * -0.270951) + (Blue * -0.315708) + (Green * -0.317263) + (Yellow * -0.242544) + (Red * -0.256463) + (RedEdge * -0.096550) + (NIR1 * -0.742535) + (NIR2 * 0.202430)
    indicesForm['WVII'] = (Green * Yellow)/(Blue * 1000)
    indicesForm['WVSI'] = (Green - Yellow)/(Green + Yellow)    

''' Requires Reflectance
    Yarbough, L. D., Navulur, K., & Ravi, R. (2014). Presentation of the Kauth-Thomas transform for Worldview-2 reflectance data.
Remote Sensing Letters, 5(2), 131-138. doi:10.1080/2150704X.2014.885148
  '''

def CalculateIndice(text, indice):
    if cbVar[indices.index(text)].get():
        print text
        indice.save(outPath + "/" + inRasterStr[:-4] + "_" + text + ".tif")

print "Exporting files"
for key,value in indicesForm.iteritems():
    CalculateIndice(key,value)

endTime = time.time() - startTime
print "Completed in", ("%.2f" % endTime), 'seconds.'
