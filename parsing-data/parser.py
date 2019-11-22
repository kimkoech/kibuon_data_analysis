
# IMPORT MODULES

import json  # json libraruy
import re
import math

# TROUBLESHOOTING
DEBUG = False


# COMPUTATION

# open, parse and covert to dict
f = open("dict_of_map", "r")

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

# get name of House Compound
name = HouseCompounds["name"]

# get the folder for each region of kibuon
folder_of_ABCD = HouseCompounds["Folder"]
kibuon_A_folder = folder_of_ABCD[0]
kibuon_B_folder = folder_of_ABCD[1]
kibuon_C_folder = folder_of_ABCD[2]
kibuon_D_folder = folder_of_ABCD[3]

# get the placemarks in each region
kibuon_A_placemarks = kibuon_A_folder["Placemark"]
kibuon_B_placemarks = kibuon_B_folder["Placemark"]
kibuon_C_placemarks = kibuon_C_folder["Placemark"]
kibuon_D_placemarks = kibuon_D_folder["Placemark"]
##############################################################################
# A placemark is a list of the houses for example :
# Each item on that list has the following structure:

# {
#"name": "A1*",
# "description": "10 adults, 1 child",
# "styleUrl": "#msn_grn-blank2",
# "Point": { "coordinates": "34.3947095051408,-1.08380898223452,0" }
#}

##############################################################################


###############################################################################


# WellSites is a list of the wells. Each item in the list has the following
# structure:

# {
#  "name": "Kandida",
#  "styleUrl": "#icon-503-4186F0-labelson-nodesc21",
#  "Point": { "coordinates": "34.3898252025247,-1.09359191436237,0"}
# }

###############################################################################

####################################################################################

# Finds distance in meters between two GPS coordinates using haversine formula
# https://nathanrooy.github.io/posts/2016-09-07/haversine-with-python/

####################################################################################

def distanceBtwn(c1, c2):
    lon1 = float(c1[0].encode())
    lat1 = float(c1[1].encode())
    lon2 = float(c2[0].encode())
    lat2 = float(c2[1].encode())

    R = 6371000                               # radius of Earth in meters
    phi_1 = math.radians(lat1)
    phi_2 = math.radians(lat2)

    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)

    a = math.sin(delta_phi / 2.0)**2 +\
        math.cos(phi_1) * math.cos(phi_2) *\
        math.sin(delta_lambda / 2.0)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    return R * c                         # output distance in meters


###############################################################################
# Compute distance from each house to each well.
# Extract max number of people
###############################################################################

# merge all house lists into one list
all_houses = kibuon_A_placemarks + \
    kibuon_B_placemarks + \
    kibuon_C_placemarks + \
    kibuon_D_placemarks

# varaible to store column headers of csv file

# TITLES
# get titles of each column
titles = "house_code,long,lat"
# compute distances and store resulting value in final CSV
for each_well in WellSites["Placemark"]:
    titles += ("," + each_well["name"])
titles += ",number_of_people"


# compute distances
output_string = ""
for each_home in all_houses:
    # get coordinates
    hs_coords = each_home["Point"]["coordinates"].split(',')
    output_string += (each_home["name"] + ", "
                      + str(hs_coords[0]) + ","
                      + str(hs_coords[1]))

    # compute distances and store resulting value in final CSV
    for each_well in WellSites["Placemark"]:
        # get coordinates of well and compute distances
        well_coords = each_well["Point"]["coordinates"].split(",")
        output_string += ("," + str(distanceBtwn(hs_coords, well_coords)))

    # extract total number of people in each house
    numbers = [int(n) for n in re.findall(r'\d+', each_home['description'])]
    max_num = 0
    # get max
    if numbers != []:
        if max(numbers) < 40:
            # store max
            max_num = max(numbers)

    output_string += ("," + str(max_num))
    # New row
    output_string += "\n"


# create and write to csv file
f = open("distances_to_wells.csv", "w+")
f.write(titles + "\n" + output_string)
f.close()


###############################################################################
# Extract distance to each water source from each house
###############################################################################

# TITLES
# get titles of each column
titles = "house_code,long,lat"
# compute distances and store resulting value in final CSV
for each_source in WaterSources["Placemark"]:
    titles += ("," + each_source["name"])


# compute distances
output_string = ""
for each_home in all_houses:
    # get coordinates
    hs_coords = each_home["Point"]["coordinates"].split(',')
    output_string += (each_home["name"] + ", "
                      + str(hs_coords[0]) + ","
                      + str(hs_coords[1]))

    # compute distances and store resulting value in final CSV
    for each_source in WaterSources["Placemark"]:
        # get coordinates of sources and compute distances
        source_coords = each_source["Point"]["coordinates"].split(",")
        output_string += ("," + str(distanceBtwn(hs_coords, source_coords)))

    # New row
    output_string += "\n"


# create and write to csv file
f = open("distances_to_water_sources.csv", "w+")
f.write(titles + "\n" + output_string)
f.close()
