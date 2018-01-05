e# file name:	SummarizeRasters.py
# author:		Jesse Langdon
# dependencies: ESRI arcpy module, Spatial Analyst extension, custom functions

import arcpy, os.path
from arcpy.sa import *
import polystat_util as u
arcpy.CheckOutExtension("SPATIAL")

arcpy.env.overwriteOutput = True

def main(in_fc, in_fc_join_field, param_tbl, fc):
    # extract values from value table
    param_str = str(param_tbl)
    param_rows = param_str.split(';')
    vt_array = []
    for r in param_rows:
        vt_array.append(r.split())
    arcpy.MakeFeatureLayer_management(in_fc, "in_fc_lyr")

    # add new fields to polygon feature class that will contain summarized stats
    param_count = len(param_rows)
    param_field_names = []
    zone_field = "ZONE_INDEX"
    for i in range(param_count):
        param_field_names.append(vt_array[i][2])
    arcpy.AddField_management("in_fc_lyr", zone_field, "TEXT")
    arcpy.CalculateField_management("in_fc_lyr", zone_field, "!" + in_fc_join_field + "!", "Python_9.3")
    ply_tmp = u.AddStatFields("in_fc_lyr", zone_field, param_field_names)

    iter_count = 0
    for j in range(param_count):
        raster_name = vt_array[j][0]
        stat_name = vt_array[j][1]
        field_name = vt_array[j][2]
        ras_lyr = arcpy.MakeRasterLayer_management(raster_name, "ras_lyr")
        zstat_result = ZonalStatisticsAsTable(ply_tmp, zone_field, ras_lyr, r"in_memory\zstat_result", "DATA", stat_name)
        u.JoinCalc(ply_tmp, zone_field, field_name, zstat_result, stat_name)
        iter_count += 1
        arcpy.AddMessage("%d of %d rasters processed..." % (iter_count, param_count))

    out_path, out_fc = os.path.split(fc)
    arcpy.FeatureClassToFeatureClass_conversion(ply_tmp, out_path, out_fc)
    del zstat_result
    arcpy.Delete_management("in_memory")
    return