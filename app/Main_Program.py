# -*- coding: utf-8 -*-
"""
Created on Thu Jun 17 10:20:37 2021

@author: matte
"""

###########################
# IMPORTS
###########################

import requests
import folium
import json
import os
import dispatch_points_and_get_area_color as dispatchModule 
import colors_on_map as colorModule


###########################
# FUNCTIONS 
###########################

def get_area_data(area_names) :
    """Get the data of every area from the area folder
    
    :param areas_names: The list of (str) names for each area.
    :type areas_names: list
    :returns: A list of list of coordinates (one sublist for each area) and a list with all the data 
    :rtype: list
    """
    area_data_list = []
    coordinates_list = []
    for name in area_names : 
        area_data_list.append(json.load(open("areas/"+ str(name))))  # we load the area file that is a .json)
    for index in range (len(area_names)) : #We go through the list of names to use every area data separately
        coordinates_list.append(area_data_list[index]['geometries'][0]['coordinates'][0][0])
    return area_data_list, coordinates_list

#-----------------------------------------------om---------------------------------------------------------------------

def choose_API_file(is_online, nb_points, local_API_name) : 
    """Choose an online or local API
    
    :param is_online: True or False, depends on the choice of the user on the web page.
    :type is_online: bool
    :param nb_points: Integer, depends on the choice of the user on the web page.
    :type nb_points: int
    :param local_API_name: The name of the local file, depends the choice of the user on the web page.
    :type local_API_name: str
    :returns: A dict with all the data from the API
    :rtype: dict
    """
    if not is_online:      # if the user check the "local" box, this condition will be False
        APIfile = json.load(open("static/"+str(local_API_name)))   # So the file used will be the local file that is input by the user.
    else:                              # if the condition 'is_online' is true 
        payload = {'rows': nb_points}    #this is a parameter, it modify the adress below to change the rows number. We found that code line on the documentation of the Requests module
        answer = requests.get('https://data.rennesmetropole.fr/api/records/1.0/search/?dataset=etat-du-trafic-en-temps-reel&q=&facet=denomination', params=payload) #this is the address of the online api, we add our parameters.
        APIfile = answer.json() 
        
    return APIfile 
    
#--------------------------------------------------------------------------------------------------------------------

def get_API_data(APIfile) :
    """Get the data from the API file chosen
    
    :param APIfile: API dict with all its data
    :type APIfile: dict
    :returns: a list of coordinates and a list of str that represent the traffic status for each point.
    :rtype: list
    """
    coordinates = []
    traffic_Status = []
    i=0
    while i < len (APIfile["records"]) :  # 'records' is the key that contains all the points so we don't want to exceed it.
        if ('geo_point_2d') not in APIfile["records"][i]["fields"] : #we found out that some points didn't have the key 'geo_point_2d' so we wrote this condition to skip them
            i+=1
        else : 
            coordinates.append(APIfile["records"][i]["fields"]['geo_point_2d'])  # [i] is the point number
            traffic_Status.append(APIfile["records"][i]["fields"]["trafficstatus"])
        i+=1
    return coordinates,traffic_Status

#--------------------------------------------------------------------------------------------------------------------

def entry (is_online, display_points, nb_points, local_API_name):   
    """The Main function that runs the other ones and our modules
    
    :param is_online: True (online API) or False (local API), depends on the choice of the user on the web page.
    :type is_online: bool
    :param display_points: True (display) or False (don't display), depends on the choice of the user on the web page.
    :type display_points: bool
    :param nb_points: Integer, depends on the choice of the user on the web page.
    :type nb_points: int
    :param local_API_name: The name of the local file, depends the choice of the user on the web page.
    :type local_API_name: str
    :returns: Nothing, directly create the html file for the map.
    """
    RennesMap = folium.Map(location=[48.117266, -1.6777926], zoom_start=12)  # Creation of the base map and location of Rennes
       
    areas_names_list = os.listdir('areas')  #Get the areas names in the 'areas' folder     
    
    area_all_data_list, polygons_coordinates = get_area_data(areas_names_list)  #Get data for every area by using their names 
       
    APIfile = choose_API_file(is_online, nb_points, local_API_name)   #We choose an online or offline API and then get data from local or online file  

    point_coordinates , point_traffic_Status = get_API_data(APIfile)  #Get coordinates and traffic status for every point on the API file 
       
    dispatchModule.traffic_points_map(point_coordinates, 'red', RennesMap, display_points)  #Choose to display the points from the API on the map 
       
    area_data_dictionary = dispatchModule.area_data_dict_creation(point_coordinates, point_traffic_Status, areas_names_list, polygons_coordinates) #creation of the dictionary with all points in each area with their traffic status
       
    area_colors_list = dispatchModule.calcul_area_color_and_grade(area_data_dictionary,areas_names_list)    #Create list with the final color of every area
   
    colorModule.color_map_display(area_colors_list, area_all_data_list, areas_names_list, RennesMap)      #Display these colors on the map with folium 
   
    folium.LayerControl().add_to(RennesMap)    #The last 2 lines that add everythin to the ma and create the html map file
    RennesMap.save("templates/Rennes_Traffic_Map.html")   #We found these lines in the folium documentation
    

###########################
# PROGRAM 
###########################

"""As we want to use the server to run the program, 
we desactivated the Main_program so nothing is returned directly by it, 
but the 2 lines below can be re-activated if we don't want to use the server
"""
   
#OnlineVersion = entry(True,True,5000,'')  # 5000 is the number of points, we can change it

#LocalVersion = entry(False,True,0,'APIfile.json')  # 'APIfile.json' is the default name of the local API file we have in our project folder
