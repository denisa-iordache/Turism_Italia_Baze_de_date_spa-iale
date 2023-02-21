import arcpy
import os

def sel_loc_dupa_drum(in_comune, in_puncte, in_railways,
                      in_sql_where,in_sql_where2, in_sql_where3,
                      out_punte_sel, out_roads_sel, out_comuna):
    """Selectarea punctelor de interes dintr-o comuna"""

    #simulare aducere oblict din baza de date in program <=> a face drag and drop tabelelor pe harta
    comune_="Comune"
    puncte_="Puncte"
    railways_ = "CaiFerate"
    arcpy.AddMessage("Se genereaza layerul comune")
    arcpy.MakeFeatureLayer_management(in_features=in_comune,
                                      out_layer=comune_)
    #arcpy.management.MakeFeatureLayer() - mod nou de scriere fara intellisense
    arcpy.AddMessage("Se genereaza layerul puncte")
    arcpy.MakeFeatureLayer_management(in_features=in_puncte,
                                      out_layer=puncte_)

    arcpy.AddMessage("Se genereaza layerul caiFerate")
    arcpy.MakeFeatureLayer_management(in_features=in_railways,
                                      out_layer=railways_)

    #selectare drum dupa un atribut
    arcpy.AddMessage("Se selecteaza punctele dupa clauza {}".format(in_sql_where))
    arcpy.SelectLayerByAttribute_management(in_layer_or_view=comune_,
                                            selection_type="NEW_SELECTION",
                                            where_clause=in_sql_where)

    #selectare localitati de-a lungul drumului
    arcpy.AddMessage("Se selecteaza punctele de interes din comuna selectata")
    puncte_com = arcpy.SelectLayerByLocation_management(in_layer=puncte_,
                                           overlap_type="WITHIN", #criteriul de selectie spatiala
                                           select_features=comune_, #ce folosesc pt conditie spatiala
                                           selection_type="NEW_SELECTION")

    drumuri_com = arcpy.SelectLayerByLocation_management(in_layer=railways_,
                                           overlap_type="WITHIN", #criteriul de selectie spatiala
                                           select_features=comune_, #ce folosesc pt conditie spatiala
                                           selection_type="NEW_SELECTION")

    arcpy.SelectLayerByAttribute_management(in_layer_or_view=puncte_com,
                                            selection_type="SUBSET_SELECTION",
                                            where_clause=in_sql_where2)

    arcpy.SelectLayerByAttribute_management(in_layer_or_view=drumuri_com,
                                            selection_type="SUBSET_SELECTION",
                                            where_clause=in_sql_where3)

    arcpy.SelectLayerByLocation_management(in_layer=puncte_com,
                                           overlap_type="WITHIN_A_DISTANCE", #criteriul de selectie spatiala
                                           select_features=drumuri_com, #ce folosesc pt conditie spatiala
                                           search_distance="2 Kilometers",
                                           selection_type="SUBSET_SELECTION")


    #creare tabela in bd
    arcpy.AddMessage("Se genereaza layerul puncte de interes selectate")
    arcpy.CopyFeatures_management(in_features=drumuri_com, out_feature_class=out_roads_sel)
    arcpy.CopyFeatures_management(in_features=puncte_com, out_feature_class=out_punte_sel)
    arcpy.CopyFeatures_management(in_features=comune_, out_feature_class=out_comuna)


    #stergere selectie
    arcpy.AddMessage("Se deseleteaza layerele puncte de interes")
    arcpy.SelectLayerByAttribute_management(in_layer_or_view=puncte_com,
                                            selection_type="CLEAR_SELECTION")
    arcpy.SelectLayerByAttribute_management(in_layer_or_view=drumuri_com,
                                            selection_type="CLEAR_SELECTION")

def ScriptTool(in_pct_sel):
    # Script execution code goes here
    nume_fc = os.path.basename(
        in_pct_sel)  # returneaza numele feature class ului (localitatile selectate); folosesc asta pt a nu folosi split
    proiect_pro = arcpy.mp.ArcGISProject("CURRENT")
    # cand se executa scriptul ia informatiile din proiectul curent pt a executa scriptul cu ele
    # acum suntem intr-un proiect
    # pt a ajunge la harta:
    harta_activa = proiect_pro.listMaps("Map")[0]
    # in loc de Map e numele hartii (ia toate hartie care incep cu Map si o afiseaza pe prima), chiar daca nu are parametru o lua pe prima
    straturi = harta_activa.listLayers()
    for strat in straturi:
        arcpy.AddMessage(
            strat.name)  # scrie starturile din harta (avem 2-drumuri, localitati; world Topo... sunt de baza, nu se pun)
    # adaug rezultatul din model pe harta
    harta_activa.addDataFromPath(in_pct_sel)
    straturi = harta_activa.listLayers()
    # adaug simbologia doar pt ultimul strat primit
    for strat in straturi:
        arcpy.AddMessage(strat.name)
        if (strat.name.upper() == nume_fc.upper()):
            # creez obiectul de tip simbologie
            simbologie = strat.symbology  # o scot pe cea existenta
            simbologie.updateRenderer(
                "UniqueValueRenderer")  # <=> intru in simbologie si in loc de single symbol am unique values
            simbologie.renderer.fields = ["type"]  # o modific
            for grp in simbologie.renderer.groups:
                for itm in grp.items:
                    if(itm.values[0][0]=="atm"):
                        itm.symbol.applySymbolFromGallery("ATM")
                    elif(itm.values[0][0]=="bank"):
                        itm.symbol.applySymbolFromGallery("Bank Account")
                    elif (itm.values[0][0] == "bar" or itm.values[0][0] == "club" or itm.values[0][0] == "nightclub" or itm.values[0][0] == "pub"):
                        itm.symbol.applySymbolFromGallery("Bar")
                    elif (itm.values[0][0] == "bus_station" or itm.values[0][0] == "bus_stop"):
                        itm.symbol.applySymbolFromGallery("Stop")
                    elif (itm.values[0][0] == "aquarium"):
                        itm.symbol.applySymbolFromGallery("Aquarium")
                    elif (itm.values[0][0] == "archaeological_s"):
                        itm.symbol.applySymbolFromGallery("Tracks")
                    elif (itm.values[0][0] == "arts_centre" or itm.values[0][0]=="artwork" or itm.values[0][0]=="attraction" or itm.values[0][0]=="museum"
                        or itm.values[0][0]=="battlefield" or itm.values[0][0]=="Begna waterfall"
                        or itm.values[0][0]=="castle" or itm.values[0][0]=="chalet" or itm.values[0][0]=="clock"
                        or itm.values[0][0]=="fountain" or itm.values[0][0]=="lighthouse" or itm.values[0][0]=="monument" or itm.values[0][0]=="palace"
                        or itm.values[0][0]=="radiotower" or itm.values[0][0]=="ruins" or itm.values[0][0]=="theatre" or itm.values[0][0]=="tower" or itm.values[0][0]=="townhall"):
                        itm.symbol.applySymbolFromGallery("Museum")
                    elif (itm.values[0][0] == "beach_resort"):
                        itm.symbol.applySymbolFromGallery("Beach")
                    elif (itm.values[0][0] == "Biblioteca Villa" or itm.values[0][0]=="library" or itm.values[0][0]=="kiosk"):
                        itm.symbol.applySymbolFromGallery("Library")
                    elif ("bicycle" in itm.values[0][0]):
                        itm.symbol.applySymbolFromGallery("Motorcycle")
                    elif (itm.values[0][0]=="cafe" or itm.values[0][0]=="restaurant" or itm.values[0][0]=="fast_food"):
                        itm.symbol.applySymbolFromGallery("Restaurant")
                    elif (itm.values[0][0] == "camp_site" or itm.values[0][0] == "caravan_site" or itm.values[0][0] == "picnic_site"):
                        itm.symbol.applySymbolFromGallery("Campground")
                    elif ("car" in itm.values[0][0]):
                        itm.symbol.applySymbolFromGallery("Car Rental")
                    elif (itm.values[0][0]=="chapel" or itm.values[0][0]=="grave_yard" or itm.values[0][0]=="memorial" or itm.values[0][0]=="place_of_worship"):
                        itm.symbol.applySymbolFromGallery("Place of Worship")
                    elif (itm.values[0][0]=="cinema"):
                        itm.symbol.applySymbolFromGallery("Shopping Center")
                    elif (itm.values[0][0] == "college" or itm.values[0][0] == "kindergarten" or itm.values[0][0] == "highschool"
                          or itm.values[0][0] == "school" or itm.values[0][0] == "school (primary)"or itm.values[0][0] == "university"):
                        itm.symbol.applySymbolFromGallery("School")
                    elif (itm.values[0][0] == "courthouse"):
                        itm.symbol.applySymbolFromGallery("Court House")
                    elif (itm.values[0][0] == "crematorium"):
                        itm.symbol.applySymbolFromGallery("Pirate")
                    elif (itm.values[0][0] == "dentist" or itm.values[0][0] == "doctor" or itm.values[0][0] == "hospital" or itm.values[0][0] == "doctors"
                        or itm.values[0][0]=="emergency_access" or itm.values[0][0]=="emergency_phone" or itm.values[0][0] == "veterinary"):
                        itm.symbol.applySymbolFromGallery("Hospital")
                    elif (itm.values[0][0] == "drinking_water"):
                        itm.symbol.applySymbolFromGallery("Droplet")
                    elif (itm.values[0][0] == "ferry_terminal"):
                        itm.symbol.applySymbolFromGallery("Ferry")
                    elif (itm.values[0][0] == "fire_station"):
                        itm.symbol.applySymbolFromGallery("Fire Station")
                    elif (itm.values[0][0] == "fuel"):
                        itm.symbol.applySymbolFromGallery("Fuel")
                    elif (itm.values[0][0] == "guest_house" or itm.values[0][0] == "hostel" or itm.values[0][0] == "hotel" or itm.values[0][0] == "motel"):
                        itm.symbol.applySymbolFromGallery("Hotel")
                    elif (itm.values[0][0] == "information"):
                        itm.symbol.applySymbolFromGallery("Information")
                    elif (itm.values[0][0] == "parking"):
                        itm.symbol.applySymbolFromGallery("Parking")
                    elif (itm.values[0][0] == "pharmacy"):
                        itm.symbol.applySymbolFromGallery("Pharmacy")
                    elif (itm.values[0][0] == "police"):
                        itm.symbol.applySymbolFromGallery("Police")
                    elif ("post" in itm.values[0][0]):
                        itm.symbol.applySymbolFromGallery("Post Office")
                    elif (itm.values[0][0]=="shop"):
                        itm.symbol.applySymbolFromGallery("Grocery Store")
                    elif ("camera" in itm.values[0][0]):
                        itm.symbol.applySymbolFromGallery("CCTV Camera")
                    elif (itm.values[0][0]=="telephone"):
                        itm.symbol.applySymbolFromGallery("Radio Tower")
                    elif (itm.values[0][0]=="theme_park" or itm.values[0][0]=="viewpoint"):
                        itm.symbol.applySymbolFromGallery("Amusement Park")
                    elif (itm.values[0][0]=="toilets"):
                        itm.symbol.applySymbolFromGallery("Restroom")
                    elif (itm.values[0][0]=="zoo"):
                        itm.symbol.applySymbolFromGallery("Zoo")
                    else:
                        itm.symbol.applySymbolFromGallery("Circle 1")
                    itm.symbol.size = 10
                    #arcpy.AddMessage(itm.values[0][0])
                    # transVal = itm.values[0][0]  # Grab the first "percent" value in the list of potential values
            strat.symbology = simbologie  # si o pun inapoi
            strat.showLabels = True
    return

if __name__ == '__main__':
    #separa defimirea functiilor de executia lor
    #drumuri=r"D:\SCOALA\Master Semestrul 1\M3 - BD Spatiale\Seminar\S1 - Dardala\Ro_proiect.gdb\drumuri" #hardcodare cale
    comune = arcpy.GetParameterAsText(0)
    puncte=arcpy.GetParameterAsText(1)
    drumuri = arcpy.GetParameterAsText(2)
    pctSel = arcpy.GetParameterAsText(6)
    drumuriSel = arcpy.GetParameterAsText(7)
    comunaSel = arcpy.GetParameterAsText(8)
    sqlWhere=arcpy.GetParameterAsText(3)
    sqlWhere2 = arcpy.GetParameterAsText(4)
    sqlWhere3 = arcpy.GetParameterAsText(5)
    sel_loc_dupa_drum(in_comune=comune,
                      in_puncte=puncte,
                      in_railways=drumuri,
                      in_sql_where=sqlWhere,
                      in_sql_where2=sqlWhere2,
                      in_sql_where3=sqlWhere3,
                      out_punte_sel=pctSel,
                      out_roads_sel=drumuriSel,
                      out_comuna=comunaSel)

    ScriptTool(in_pct_sel=pctSel)
