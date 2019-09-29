
# IMPORT MODULES

import json  # json libraruy

# TROUBLESHOOTING



# COMPUTATION

# open, parse and covert to dict
f = open("raw-data/dumped_json_of_map", "r")

str_representation = f.read()

f.close()

mapDict = json.loads(str_representation)

# retrieve name and coordinates pair

GeoBorders = mapDict["kml"]["Document"]["Folder"]["Folder"][0]
HouseCompounds = mapDict["kml"]["Document"]["Folder"]["Folder"][1]
Landmarks = mapDict["kml"]["Document"]["Folder"]["Folder"][2]
Latrines = mapDict["kml"]["Document"]["Folder"]["Folder"][3]
WaterSources = mapDict["kml"]["Document"]["Folder"]["Folder"][4]
WellSites = mapDict["kml"]["Document"]["Folder"]["Folder"][5]
Supplies = mapDict["kml"]["Document"]["Folder"]["Folder"][6]

# House compounds
name = HouseCompounds["name"]

folder_of_ABCD = HouseCompounds["Folder"]
kibuon_A_folder = folder_of_ABCD[0]
kibuon_B_folder = folder_of_ABCD[1]
kibuon_C_folder = folder_of_ABCD[2]
kibuon_D_folder = folder_of_ABCD[3]

print(kibuon_A_folder)

kibuon_A_placemarks = kibuon_A_folder["Placemark"]


for each_home_in_A in kibuon_A_placemarks:
	# name and coordinates
	print(str(each_home_in_A["name"]) + "  " + str(each_home_in_A["Point"]))


# well sites
print(" ~~~~~ WELL SITES ~~~~~~")
print(WellSites["Placemark"])

# find the displacement well Sites and these geopoints



#


