# -*- coding: utf-8 -*-
"""
Created on Sat Jun 19 21:56:02 2021

@author: leobu
"""

#######################################
#module 
#######################################
"""This module is the major part of the program,
it's used to dispatch every point in its polygon and then determine a general color 
for every polygon
"""

import folium



def traffic_points_map(coordList,color, myMap, display_points) :
    """Allow the user to choose to display or not the data points on the map
    
    :param coordList: The list of (lon, lat) for all the data points.
    :type coordList: list
    :param color: The color we want for the points.
    :type color: str
    :param myMap: The folium map  
    :type myMap: folium.folium.map
    :param display_points: True if the user checked yes on the web page or False otherwise
    :type display_points: bool
    :returns: Nothing, just display (or not) the points directly on the map using folium
    """
    if display_points :    # if the entry is True, (means the user checked the 'yes' case)
        for coords in coordList:    # for every point, we display it on the map 
            folium.CircleMarker(    # we found this code in the folium documentation and adapted it
                    location=coords,
                    radius=1,
                    color=color,
                    fill=True,
                    fill_color=color,
                    ).add_to(myMap)
    
#--------------------------------------------------------------------------------------------------------------------

def is_point_in_poly(coord_point,coord_polygon):
    """Check if a point is inside a polygon
    
    :param coord_point: A tuple with (lon, lat) values.
    :type coord_point: tuple
    :param coord_polygon: The list of (lon, lat) values of a polygon.
    :type coord_polygon: list
    :returns: True if the point is inside the polygon, False otherwise
    :rtype: bool
    """
    
    nombre_sommets = len(coord_polygon)  
    inside = False  
    counter = 0
    p1x,p1y = coord_polygon[0]   
    i=0
    while i<nombre_sommets : 
        p2x,p2y = coord_polygon[i]
        if coord_point[0] > min(p1y,p2y) and coord_point[0] <= max(p1y,p2y) :  # if Y(a) between Y(p1) and Y(p2) 
                if coord_point[1] <= max(p1x,p2x):                             # and if X(a) < maximum (can be X(p1) or X(p2)) 
                    if p1y != p2y :  #div par 0
                         abscisseB = (p2x-p1x)*((p1y-coord_point[0])/(p1y-p2y))-(coord_point[1]-p1x)  #this line results from the Thalès theorem, we explain it precisely in the report 
                    if p1x == p2x or coord_point[1] <= abscisseB:        # else if p1x p2x is a vertical line or if X(a) < X(b)
                        counter +=1     #means the line that start from the point croses a segment of the polygon, so we add 1 to the counter
        p1x,p1y = p2x,p2y
        i+=1
    if counter %2 != 0 : #If the counter is odd, then the point is inside the polygon
        inside = True
    
    return inside    

#--------------------------------------------------------------------------------------------------------------------

def area_data_dict_creation(point_coordsList, traffic_Status, areas_names, area_coordinates) :
    """Creates a dictionary to gather all the data
    
    :param point_coordsList: The list of (lon, lat) for all the data points.
    :type point_coordsList: list
    :param traffic_Status: The list of (str) traffic status values for each point.
    :type traffic_Status: list
    :param areas_names: The list of (str) names for each area.
    :type areas_names: list
    :param area_coordinates: The list of (lon, lat) values for every area.
    :type area_coordinates: list
    :return: Dictionary with every name as keys and for each name a second dictionary with every traffic status and the points associated.
    :rtype: dict
    """
    
    area_data_dict = {}        
   
    for area_nb in range(len(areas_names)) :  #We go through every area
        freeflowList = []      #We set every list and the traffic dictionary to empty
        heavyList = []
        congestedList = []
        impossibleList = []
        total_coord = []
        TrafficStatusDict = {}
        
        for index in range(len(point_coordsList)) :  #For each area, we review each point from the points coordinates list
    
            if is_point_in_poly(point_coordsList[index],area_coordinates[area_nb]) :  # we use ou function is_point_in_poly to determine if our current point is in our current area
                                
                if traffic_Status[index] == "freeFlow" :      # If for the current index, the traffic_status value is 'freeFlow' :  
                    freeflowList.append(point_coordsList[index])  # we add the current [X,Y] coordinates to the freeflow list.
                
                if traffic_Status[index] == "heavy" :         #Same for each status, except unknown that we chose to ignore
                    heavyList.append(point_coordsList[index])
    
                if traffic_Status[index] == "congested" :
                    congestedList.append(point_coordsList[index])
    
                if traffic_Status[index] == "impossible" :
                    impossibleList.append(point_coordsList[index])
                
                total_coord.append((point_coordsList[index]))    #Then a final list is created with all the points coord for the current polygon
            else :     #If the function returns False, we do nothing and pass to the next point
                pass
        
        TrafficStatusDict["freeFlow"] = freeflowList  #We add every liste to its key in our 2nd dictionary
        TrafficStatusDict["heavy"] = heavyList
        TrafficStatusDict["congested"] = congestedList
        TrafficStatusDict["impossible"] = impossibleList
        TrafficStatusDict["total_points"] = total_coord
        
        
        area_data_dict[str(areas_names[area_nb])] =  TrafficStatusDict  #We add our dictionary to the current area key in our main dict and restart the process with the next area
 
        
    return area_data_dict   

#--------------------------------------------------------------------------------------------------------------------

def calcul_area_color_and_grade(dictionary,areas_names) : 
    """Calcul the color of an area based on all the points in it
    
    :param dictionary: The dictionary generated by the function 'area_data_dict_creation'.
    :type dictionary: dict
    :param areas_names: The list of (str) names for each area.
    :type areas_names: list
    :returns: a list of colors, in the order of the areas names list.
    :rtype: list
    """
    area_colors = []
    area_nb = 0
    while area_nb < len(areas_names) :   
        
        overall_size =len(dictionary[str(areas_names[area_nb])]["total_points"])            
        grade_freeflow = len(dictionary[str(areas_names[area_nb])]["freeFlow"]) * 20     #we multiply the number of points in each category by its grade            
        grade_heavy = len(dictionary[str(areas_names[area_nb])]["heavy"]) * 12              
        grade_congested = len(dictionary[str(areas_names[area_nb])]["congested"]) * 8          
        grade_impossible = len(dictionary[str(areas_names[area_nb])]["impossible"]) * 0
        
        if overall_size != 0:      #if there is no point in a polygon, overall_size == 0 and we can't divide by 0
            average_grade =  (grade_freeflow + grade_heavy + grade_congested + grade_impossible) / overall_size  # We calcul the average
        else:
            average_grade = 30 # renders white if there is no data in an area
            
        if 0 <= average_grade < 5 :         # we append the color of the current area depending on the average grade 
            area_colors.append("#000000")   #HTML color code     
        elif 5 <= average_grade < 10 :
            area_colors.append("#f91f05")     
        elif 10 <= average_grade < 15:
            area_colors.append("#f9b605")
        elif 15 <= average_grade <= 20 :
            area_colors.append("#1bd33c")
        elif average_grade == 30 : 
            area_colors.append("#FFFFFF")                  
        area_nb+=1
        
    return area_colors