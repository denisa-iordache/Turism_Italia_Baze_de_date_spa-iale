import arcpy
import os


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


# This is used to execute code if the file was run but not imported
if __name__ == '__main__':
    # Tool parameter accessed with GetParameter or GetParameterAsText
    sel_loc = arcpy.GetParameterAsText(0)

    ScriptTool(in_pct_sel=sel_loc)

    # Update derived parameter values using arcpy.SetParameter() or arcpy.SetParameterAsText()