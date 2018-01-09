# PolyStat Tools -- Summarize Rasters

## Summary

**Summarize Rasters** is a tool within **PolyStat Tools**, which is an ArcGIS Python toolbox. The **Summarize Rasters** tool 
take a polygon feature class, overlays the feature class on one or more raster datasets, and summarizes the values associated
 with the raster grid cells intersecting each polygon. Each set of summarized values is then joined to the attribute table of the 
 feature class as a new field, with each field representing the values from a summarized raster dataset.

This tool is written in Python, and uses ESRI's ArcPy package extensively.

## Downloads

[PolyStat Tools, v0.2](Downloads/PolyStat02.zip)

## Updates and Release Notes

1/8/2018

* Release PolyStat Tool, v0.2
    * Refactored Summarize Rasters tool allow processing of overlapping polygons.
    * Improved error handling.

11/29/2015

* Release PolyStat Tool, v0.1
    * Initial public release
    * Includes basic XML help file

## Geoprocessing Environment

* This tool was built using Python 2.7 and only works with ArcGIS *10.3 or higher*.
* The tool can run in a 64-bit geoprocessing environment.

## Data Input Requirements

1. **Input polygon feature class**: A polygon feature class that encompasses the area of analysis.
2. **Zone field**: Attribute field in the input polygon feature class that serves as a unique identifier field.  This field will be converted to a new field called "ZONE_INDEX" in the output feature class.
3. **Summary data list**: The list of raster datasets that will be summarized.  The user is required to add three values for each raster that is added:
    * Raster Dataset - the file path to the raster dataset
    * Statistic Type - the type of statistical summary that will be performed for that raster datasets, i.e. mean, maximum, minimum, etc.
    * Summary Field Name - the name that will be assigned to the field which will contain the summarized values.
4. **Output feature class**: the file path and name of the polygon feature class that will be output from the tool.

### Please Note
If the grid cell size of a raster dataset is larger than the minimum size of polygon features in the feature class, the output feature class may have blank values for those polygon features.


## Acknowledgements
The PolyStat Tools toolbox is developed and maintained by [Jesse Langdon](mailto:jesselangdon@gmail.com).