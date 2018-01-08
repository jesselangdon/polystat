# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Name:        PolyStat Tools                                                 #
# Purpose:     Tools for summarizing data by a polygon feature class.         #
#                                                                             #
# Author:      Jesse Langdon                                                  #
#              Seattle, Washington                                            #
#                                                                             #
# Created:     2015-Oct-26                                                    #
# Version:     0.1                                                            #
# Modified:    2018-Jan-5                                                     #
# Copyright:   Jesse Langdon 2018                                             #
# License:     MIT                                                            #
#                                                                             #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#!/usr/bin/env python

# Import modules
import arcpy
import polystat as ps

class Toolbox(object):
    def __init__(self):
        """Define the toolbox (the name of the toolbox is the name of the .pyt file)."""
        self.label = "PolyStat Tools"
        self.alias = "PolyStat Tools"

        # List of tool classes associated with this toolbox
        self.tools = [SummarizeRastersTool]


class SummarizeRastersTool(object):
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "Summarize Rasters"
        self.description = "The Summarize Rasters tool takes any polygon dataset as an input, and statistically " \
                           "summarizes user-selected attributes per polygon feature for one or more raster datasets" \
                           " that intersect that polygon.  As an example, the user could specify a polygon dataset" \
                           " representing watersheds. The tool could calculate the mean elevation found within each" \
                           " watershed polygon, based on a spatially coincident digital elevation model."
        self.canRunInBackground = True

    def getParameterInfo(self):
        """Define parameter definitions"""
        param0 = arcpy.Parameter(
            displayName='Input polygon feature class',
            name='in_ply',
            datatype='Feature Class',
            parameterType='Required',
            direction='Input')
        param0.filter.list = ['Polygon']

        param1 = arcpy.Parameter(
            displayName='Zone field',
            name='in_fc_join_field',
            datatype='Field',
            parameterType='Required',
            direction='Input')
        param1.parameterDependencies = [param0.name]

        param2 = arcpy.Parameter(
            displayName='Do the input polygon features overlap (e.g. upstream catchments)?',
            name='bool_overlap',
            datatype='GPBoolean',
            parameterType='Optional',
            direction='Input')

        param3 = arcpy.Parameter(
            displayName='Summary parameter data list',
            name='stat_list',
            datatype='GPValueTable',
            parameterType='Required',
            direction='Input')
        param3.columns = [['Raster Dataset','Raster Dataset'], ['GPString','Statistic Type'], ['GPString', 'Summary Field Name']]
        param3.filters[1].type = 'ValueList'
        param3.filters[1].list = ['MEAN', 'MAXIMUM', 'MINIMUM', 'RANGE', 'STD', 'SUM']

        param4 = arcpy.Parameter(
            displayName='Output feature class',
            name='out_fc',
            datatype='DEFeatureClass',
            parameterType='Required',
            direction='Output')

        params = [param0, param1, param2, param3, param4]
        return params

    def isLicensed(self):
        """Set whether tool is licensed to execute."""
        return True

    def updateParameters(self, parameters):
        """Modify the values and properties of parameters before internal
        validation is performed.  This method is called whenever a parameter
        has been changed."""
        return

    def updateMessages(self, parameters):
        """Modify the messages created by internal validation for each tool
        parameter.  This method is called after internal validation."""
        return

    def execute(self, parameters, messages):
        """The source code of the tool."""



        ps.main(parameters[0].valueAsText,
                parameters[1].valueAsText,
                parameters[3].valueAsText,
                parameters[4].valueAsText,
                parameters[2].valueAsText)

        return

# # TEST
# def main():
#     tool = SummarizeRastersTool()
#     tool.execute(tool.getParameterInfo(), None)
#
# if __name__ == '__main__':
#     main()


# # TEST
# vt = arcpy.ValueTable(3)
# vt.addRow('C:\\JL\\Testing\\polystat\\input\\elev10m_lemhi.tif MEAN elev_mean')
# vt.addRow('C:\\JL\\Testing\\polystat\\input\\nbcd_baw.tif MAXIMUM veg_max')
#
# in_poly = r"C:\JL\Testing\polystat\input\poly_overlap.shp"
# zone_field = "LineOID"
# bool_overlap = True
# out_poly = r"C:\JL\Testing\polystat\input\test_overlap.shp"

# ps.main(in_poly, zone_field, vt, out_poly, bool_overlap)