# Derive Remote Sensing Indices

Takes stacked raster imagery to calculate common remote sensing indices and export individual bands.

Sensors supported:

* Landsat 4-5 TM
* Landsat 7 ETM+
* Landsat 8 OLI
* Worldview-02
* MODIS Terra and Aqua

Available indices to calculate (sensor dependent):
* [NDVI (Normalized Difference Vegetation Index)] (http://www.indexdatabase.de/db/i-single.php?id=58)
* [NDMI (Normalized Difference Moisture Index)] (http://www.indexdatabase.de/db/i-single.php?id=56)
* [NDSI (Normalized Difference Soil Index)] (http://www.exelisvis.com/portals/0/pdfs/envi/8_bands_Antonio_Wolf.pdf)
* [NDWI (Normalized Difference Water Index)] (http://www.indexdatabase.de/db/i-single.php?id=60)
* [MNDWI (Modified Normalized Difference Water Index)] (http://www.tandfonline.com/doi/abs/10.1080/01431160600589179)
* [SAVI (Soil Adjusted Vegetation Index)] (http://www.indexdatabase.de/db/i-single.php?id=87)
* [MSAVI2 (Modified Soil Adjusted Vegetation Index 2)] (http://www.sciencedirect.com/science/article/pii/0034425794901341)
* [NBR (Normalized Burn Ratio)] (http://www.indexdatabase.de/db/i-single.php?id=53)
* [NMDI (Normalized Multi-band Drought Index)] (http://onlinelibrary.wiley.com/doi/10.1029/2007GL031021/abstract)
* [NHFD (Non-Homogenous Feature Difference (NHFD)] (http://www.exelisvis.com/portals/0/pdfs/envi/8_bands_Antonio_Wolf.pdf)
* [Tasseled Cap Transformation - Brightness, Greenness, Wetness] (http://docs.lib.purdue.edu/cgi/viewcontent.cgi?article=1160&context=lars_symp&sei-redir=1&referer=http%3A%2F%2Fscholar.google.com%2Fscholar%3Fhl%3Den%26q%3Dkauth%20and%20thomas#search=%22kauth%20thomas%22)

Uses a GUI interface developed in Tkinter.


