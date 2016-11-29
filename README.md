## Remote Sensing Indices Derivation Tool

Processes a stacked raster file to calculate spectral remote sensing indices and export individual bands.

**Sensors supported:**

* Landsat 1-5 MSS
* Landsat 4-5 TM
* Landsat 7 ETM+
* Landsat 8 OLI
* Worldview-02
* MODIS Terra and Aqua

**Indices supported (sensor dependent):**

Vegetation Related Indices

* [NDVI (Normalized Difference Vegetation Index)] (http://www.indexdatabase.de/db/i-single.php?id=58)
* [SAVI (Soil Adjusted Vegetation Index)] (http://www.indexdatabase.de/db/i-single.php?id=87)
* [EVI (Enhanced Vegetation Index)] (http://www.indexdatabase.de/db/i-single.php?id=16)
* [EVI2 (Enhanced Vegetation Index 2)] (http://www.indexdatabase.de/db/i-single.php?id=237)
* [NDMI (Normalized Difference Moisture Index)] (http://www.indexdatabase.de/db/i-single.php?id=56)
* [NMDI (Normalized Multi-band Drought Index)] (http://onlinelibrary.wiley.com/doi/10.1029/2007GL031021/abstract)

Hydrologic Indices

* [NDWI (Normalized Difference Water Index)] (http://www.indexdatabase.de/db/i-single.php?id=60)
* [MNDWI (Modified Normalized Difference Water Index)] (http://www.tandfonline.com/doi/abs/10.1080/01431160600589179)

Geologic/Soil Indices

* [Clay Minerals Ratio] (http://library.dmr.go.th/library/TextBooks/10146.pdf)
* [Ferrous Minerals Ratio] (http://library.dmr.go.th/library/TextBooks/10146.pdf)
* [Iron Oxide Ratio] (https://scholar.google.com/scholar?cluster=2710721694487237686&hl=en&as_sdt=4005&sciodt=0,6)
* [WV-II (World-View New Iron Index)] (http://www.exelisvis.com/portals/0/pdfs/envi/8_bands_Antonio_Wolf.pdf)
* [WV-SI (World-View Soil Index)] (http://www.exelisvis.com/portals/0/pdfs/envi/8_bands_Antonio_Wolf.pdf)

Burn Indices

* [NBR (Normalized Burn Ratio)] (http://www.indexdatabase.de/db/i-single.php?id=53)
* [BAI (Burn Area Index)] (http://www.tandfonline.com/doi/abs/10.1080/01431160210153129)

Miscellaneous Indices

* [NDBI (Normalized Difference Built-Up Index)] (http://www.tandfonline.com/doi/abs/10.1080/01431160304987)
* [NHFD (Non-Homogenous Feature Difference (NHFD)] (http://www.exelisvis.com/portals/0/pdfs/envi/8_bands_Antonio_Wolf.pdf)
* [NDSI (Normalized Difference Snow Index)] (http://ieeexplore.ieee.org/xpls/abs_all.jsp?arnumber=399618&tag=1)

[Tasseled Cap Transformation] (http://docs.lib.purdue.edu/cgi/viewcontent.cgi?article=1160&context=lars_symp&sei-redir=1&referer=http%3A%2F%2Fscholar.google.com%2Fscholar%3Fhl%3Den%26q%3Dkauth%20and%20thomas#search=%22kauth%20thomas%22)

* Brightness, Greenness, Wetness, Yellowness (MSS) 
  * Reflectance required for TM, ETM+, OLI, WV02, and MODIS
  * Digital Number (DN) required for MSS

## Requirements

**arcpy version**

Requires arcpy and [Tkinter] (https://wiki.python.org/moin/TkInter). 

**GDAL version**

Requires [GDAL Calculations] (https://pypi.python.org/pypi/gdal-calculations) and [Tkinter] (https://wiki.python.org/moin/TkInter). 

## Instructions

Run the arcpy or GDAL Python script and use the GUI to select the satellite sensor, indices to calculate, input raster, and output path. Be sure Sensors_Formulas_RSIDT.ini is in the same directory.

<p align="center">
  <img src="https://github.com/rander38/Remote-Sensing-Indices-Derivation-Tool/blob/master/Documentation/GUI.PNG" alt="Interface"/>
</p>

**Input raster should be stacked as follows (or manually adjust band designations within Python script)**

*Landsat 1-5 MSS*

* Green - Red - NIR1 - NIR2


*Landsat 4-5 TM/Landsat 7 ETM+:*

* Blue - Green - Red - NIR - SWIR1 - SWIR2


*Landsat 8 OLI:*

* Coastal - Blue - Green - Red - NIR - SWIR1 - SWIR2


*MODIS:*

* Red - NIR - Green - Blue - SWIR1 - SWIR2 - SWIR3


*Worldview 02:*

* Coastal - Blue - Green - Yellow - Red - Red Edge - NIR1 - NIR2


**Manually Add an Index**

Open the file, Sensors_Formulas_RSIDT.ini

In [Parameters], add the name of the index to the indices list, add the index with compatible sensors to the indicesSensor dictionary. 

In [Formulas], add the index with equation.

### Future Plans

* Additional Sensors/Indices (Requests are welcome)
* QGIS/ArcGIS Toolbox

### Works Cited
  Baig, M. H. A., Zhang, L., Shuai, T., & Tong, Q. (2015). Derivation of a tasselled cap transformation 
based on Landsat 8 at-satellite reflectance. Remote Sensing Letters, 5(5), 423–431. doi:10.1080/2150704X.2014.915434

  Chuvieco, E., Martín, M. P., & Palacios, A. (2002). Assessment of different spectral indices in the red-near-infrared spectral domain for burned land discrimination. International Journal of Remote Sensing, 23(23), 5103–5110. doi:10.1080/01431160210153129

  Crist, E. P. (1985). A TM Tasseled Cap equivalent transformation for reflectance factor data. Remote Sensing of Environment, 17(3), 301–306. doi:10.1016/0034-4257(85)90102-6
  
  Drury, S. (1987). Image Interpretation in Geology. London: Allen and Unwin.
  
  Huang, C., Wylie, B., Yang, L., Homer, C., & Zylstra, G. (2002). Derivation of a tasselled cap transformation based on Landsat 7 at-satellite reflectance. International Journal of Remote Sensing, 23(8), 1741–1748. doi:10.1080/01431160110106113

  Huete, A. . (1988). A soil-adjusted vegetation index (SAVI). Remote Sensing of Environment, 25(3), 295–309. doi:10.1016/0034-4257(88)90106-X

  Kauth, R., & Thomas, G. (1976). The tasselled cap--a graphic description of the spectral-temporal development of agricultural crops as seen by Landsat. LARS Symposia.

  Qi, J., Chehbouni, A., Huete, A. R., Kerr, Y. H., & Sorooshian, S. (1994). A modified soil adjusted vegetation index. Remote Sensing of Environment, 48(2), 119–126. doi:10.1016/0034-4257(94)90134

  Riggs, G. A., Hall, D. K., & Salomonson, V. V. (1994). A snow index for the Landsat Thematic Mapper and Moderate Resolution Imaging Spectroradiometer. In Proceedings of IGARSS ’94 - 1994 IEEE International Geoscience and Remote Sensing Symposium (Vol. 4, pp. 1942–1944). IEEE. doi:10.1109/IGARSS.1994.399618

  Roy, D. P., Boschetti, L., & Trigg, S. N. (2006). Remote Sensing of Fire Severity: Assessing the Performance of the Normalized Burn Ratio. IEEE Geoscience and Remote Sensing Letters, 3(1), 112–116. doi:10.1109/LGRS.2005.858485

  Tucker, C. J. (1979). Red and photographic infrared linear combinations for monitoring vegetation. Remote Sensing of Environment, 8(2), 127–150. doi:10.1016/0034-4257(79)90013-0

  Wang, L., & Qu, J. J. (2007). NMDI: A normalized multi-band drought index for monitoring soil and vegetation moisture with satellite remote sensing. Geophysical Research Letters, 34(20), L20405. doi:10.1029/2007GL031021

  Wilson, E. H., & Sader, S. A. (2002). Detection of forest harvest type using multiple dates of Landsat TM imagery. Remote Sensing of Environment, 80(3), 385–396. doi:10.1016/S0034-4257(01)00318-2

  Yarbrough, L. D., Navulur, K., & Ravi, R. (2014). Presentation of the Kauth–Thomas transform for WorldView-2 reflectance data. Remote Sensing Letters, 5(2), 131–138. doi:10.1080/2150704X.2014.885148

  Zha, Y., Gao, J., & Ni, S. (2003). Use of normalized difference built-up index in automatically mapping urban areas from TM imagery. International Journal of Remote Sensing, 24(3), 583–594. doi:10.1080/01431160304987

  Zhang, X. Z. X., Schaaf, C. B., Friedl, M. a., Strahler, a. H., Gao, F. G. F., & Hodges, J. C. F. (2002). MODIS tasseled cap transformation and its utility. IEEE International Geoscience and Remote Sensing Symposium, 2(C), 1063–1065. doi:10.1109/IGARSS.2002.1025776

### License

The MIT License (MIT)

Copyright (c) 2015 Ryan S. Anderson
	
Permission is hereby granted, free of charge, to any person obtaining a copy of
this software and associated documentation files (the "Software"), to deal in
the Software without restriction, including without limitation the rights to
use, copy, modify, merge, publish, distribute, sublicense, and to permit persons 
to whom the Software is furnished to do so, subject to the following conditions:
	
The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.
	
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER
IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

**Contact: ryananderson57@gmail.com**
