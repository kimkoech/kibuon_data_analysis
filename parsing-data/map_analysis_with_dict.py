
# IMPORT MODULES

import json  # json libraruy
import re

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


####################################################################################

# Finds distance in meters between two GPS coordinates using haversine formula
# https://nathanrooy.github.io/posts/2016-09-07/haversine-with-python/

####################################################################################

def distanceBtwn(c1, c2):
    lon1 = c1[0]
    lat1 = c1[1]
    lon2 = c2[0]
    lat2 = c2[1]

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
# Compute the distance between each well
###############################################################################
# clear any existent file
f = open("population.txt", "w+")
for each_home_in_A in kibuon_A_placemarks:
    # get numbers in each house
    numbers = [int(n) for n in re.findall(r'\d+', each_home_in_A['description'])]
    numbers2 = [int(n) for n in re.findall(r'\d+', each_home_in_A['name'])]
    max_num = 0
    # get max
    if numbers != []:
        if max(numbers) < 40:
            # store max
            max_num = max(numbers)

    # print name and coordinates
    line = str(max(numbers2)) + "," + str(each_home_in_A["Point"]["coordinates"]) + str(max_num) + "\n"
    print(line)
    f.write(line)

f.close()


###############################################################################


# WellSites is a list of the wells. Each item in the list has the following
# structure:

# {
#  "name": "Kandida",
#  "styleUrl": "#icon-503-4186F0-labelson-nodesc21",
#  "Point": { "coordinates": "34.3898252025247,-1.09359191436237,0"}
# }

###############################################################################


###############################################################################
# Example code for how to print the coordinates of each well site:
###############################################################################


for each_item in WellSites["Placemark"]:
    print(str(each_item["name"]) + " " + str(each_item["Point"]))


# To do: find the distance between each well and each house
