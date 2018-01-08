import arcpy

def add_stat_fields(in_fc_lyr, in_fc_join_field, stat_list):
    ply_add = arcpy.FeatureClassToFeatureClass_conversion(in_fc_lyr, "in_memory", "poly_stat")
    cur_field_obj = arcpy.ListFields(in_fc_lyr)
    cur_field_names = []
    for f in cur_field_obj:
        if not f.type == "Geometry" and not f.type == "OID" and not f.name == in_fc_join_field:
            cur_field_names.append(str(f.name))
    arcpy.DeleteField_management(ply_add, cur_field_names)
    for i in stat_list:
        arcpy.AddField_management(ply_add, i, "DOUBLE")
    return ply_add

#def JoinCalc(to_fc, to_join_field, to_attr_field, from_tbl, from_join_field, from_attr_field):
def join_calc(to_fc, join_field, to_attr_field, from_tbl, from_attr_field):
    ''' Using dictionaries, this function updates a single attribute
    field in a feature class based on a field in another feature
    class. Can be used as an alternative to the AddJoin and
    CalculateField functions in arcpy module.'''
    import arcpy
    #create dictionary based on 'from_tbl' value table
    from_fields = [join_field, from_attr_field]
    from_dict = {}
    with arcpy.da.SearchCursor(from_tbl, from_fields) as f_cursor:
        for f_row in f_cursor:
            from_join_val = f_row[0]
            from_attr_val = f_row[1]
            from_dict[from_join_val] = from_attr_val

    # update attribute field in to_fc if join fields are equal
    to_fields = [join_field, to_attr_field]
    with arcpy.da.UpdateCursor(to_fc, to_fields) as t_cursor:
        for t_row in t_cursor:
            to_join_val = t_row[0]
            if from_dict.has_key(to_join_val):
                t_row[1] = from_dict[to_join_val]
            t_cursor.updateRow(t_row)
    return to_fc

def clear_inmemory():
    """Clears all in_memory datasets."""
    arcpy.env.workspace = r"IN_MEMORY"
    arcpy.AddMessage("Deleting in_memory data...")

    list_fc = arcpy.ListFeatureClasses()
    list_tbl = arcpy.ListTables()

    # for each FeatClass in the list of fcs's, delete it.
    for f in list_fc:
        arcpy.Delete_management(f)
    # for each TableClass in the list of tab's, delete it.
    for t in list_tbl:
        arcpy.Delete_management(t)
    return
