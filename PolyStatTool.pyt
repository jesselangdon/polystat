# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Name:        PolyStat Toolbox                                               #
# Purpose:     Tools for summarizing raster data by a polygon dataset.        #
#                                                                             #
# Author:      Jesse Langdon                                                  #
#              Seattle, Washington                                            #
#                                                                             #
# Created:     2015-Oct-26                                                    #
# Version:     0.1          Modified:                                         #
# Copyright:   (c) Jesse Langdon 2015                                         #
# License:                                                                    #
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
        self.tools = [summarizeRasters]


class summarizeRasters(object):
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
            displayName='Summary data list',
            name='stat_list',
            datatype='GPValueTable',
            parameterType='Required',
            direction='Input')
        param2.columns = [['Raster Dataset','Raster Dataset'], ['GPString','Statistic Type'], ['GPString', 'Summary Field Name']]
        param2.filters[1].type = 'ValueList'
        param2.filters[1].list = ['MEAN', 'MAXIMUM', 'MINIMUM', 'RANGE', 'STD', 'SUM']

        param3 = arcpy.Parameter(
            displayName='Output feature class',
            name='out_fc',
            datatype='DEFeatureClass',
            parameterType='Required',
            direction='Output')

        params = [param0, param1, param2, param3]
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
                parameters[2].valueAsText,
                parameters[3].valueAsText)
        return