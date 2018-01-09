# File Name:	SummarizeRasters.py
# Author:		Jesse Langdon
# Revised:      1/5/2018
# Dependencies: ESRI arcpy module, Spatial Analyst extension, custom functions

import gc
import os.path
import arcpy
from arcpy.sa import *
import polystat_util as u

if arcpy.CheckExtension("SPATIAL") == "Available":
        arcpy.CheckOutExtension("SPATIAL")
else:
    arcpy.AddError("PolyStat: Summarize Rasters tool requires Spatial Analyst. License currently unavailable.")

arcpy.env.overwriteOutput = True
gc.enable()

# CONSTANTS
summary_names = {} #There are a couple of inconsistencies with how ZonalStatistics fields
summary_names["MAXIMUM"] = "MAX"
summary_names["MINIMUM"] = "MIN"
summary_names["MEAN"] = "MEAN"
summary_names["RANGE"] = "RANGE"
summary_names["STD"] = "STD"
summary_names["SUM"] = "SUM"

def calc_params(in_zone, zone_field, vt_array, param_count):
    # iterate through raster parameters and calculate zonal statistics
    iter_count = 0
    for j in range(param_count):
        raster_name = vt_array[j][0]
        stat_name = vt_array[j][1]
        field_name = vt_array[j][2]
        ras_lyr = arcpy.MakeRasterLayer_management(raster_name, "ras_lyr")
        try:
            zstat_result = ZonalStatisticsAsTable(in_zone, zone_field, ras_lyr, r"in_memory\zstat_result",
                                               "DATA", stat_name)
            u.join_calc(in_zone, zone_field, field_name, zstat_result, summary_names[stat_name])
            iter_count += 1
            arcpy.AddMessage("{0} of {1} rasters processed...".format(iter_count, param_count))
            del zstat_result
        except Exception as e:
            arcpy.AddMessage("Problem summarizing for polygon feature {0}".format(in_zone))
            arcpy.AddMessage(e)
            continue
    return

def main(in_fc, in_fc_join_field, param_tbl, out_fc, bool_overlap=False):
    # extract values from value table
    param_str = str(param_tbl)
    param_rows = param_str.split(';')
    vt_array = []
    for r in param_rows:
        vt_array.append(r.split())
    in_fc_lyr = "in_fc_lyr"
    arcpy.MakeFeatureLayer_management(in_fc, in_fc_lyr)

    # add new fields to polygon feature class that will contain summarized stats
    param_count = len(param_rows)
    param_field_names = []
    zone_field = "ZONE_INDEX"
    for i in range(param_count):
        param_field_names.append(vt_array[i][2])
    arcpy.AddField_management(in_fc_lyr, zone_field, "TEXT")
    arcpy.CalculateField_management(in_fc_lyr, zone_field, "!" + in_fc_join_field + "!", "Python_9.3")
    ply_tmp = u.add_stat_fields(in_fc_lyr, zone_field, param_field_names)
    ply_tmp_lyr = "ply_tmp_lyr"
    arcpy.MakeFeatureLayer_management(ply_tmp, ply_tmp_lyr)

    if bool_overlap == True:
        # iterate through polygons if overlapping
        arcpy.AddMessage("Iterating through overlapping polygons...")
        with arcpy.da.SearchCursor(ply_tmp_lyr, [zone_field]) as cursor:
            for row in cursor:
                expr = """"{0}" = '{1}'""".format(zone_field, row[0])
                arcpy.SelectLayerByAttribute_management(ply_tmp_lyr, "NEW_SELECTION", expr)
                ply_select_lyr = "ply_select_lyr"
                arcpy.MakeFeatureLayer_management(ply_tmp_lyr, ply_select_lyr)
                calc_params(ply_select_lyr, zone_field, vt_array, param_count)
                arcpy.AddMessage("Polygon with {0}:{1} processed".format(zone_field, row[0]))
                arcpy.SelectLayerByAttribute_management(ply_tmp_lyr, "CLEAR_SELECTION")
    else:
        calc_params(ply_tmp_lyr, zone_field, vt_array, param_count)

    out_path, out_fc = os.path.split(out_fc)
    arcpy.FeatureClassToFeatureClass_conversion(ply_tmp_lyr, out_path, out_fc)

    u.clear_inmemory()
    arcpy.CheckInExtension("SPATIAL")

    return