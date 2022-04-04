# -*- coding: utf-8 -*-
"""
Created on Sun Jun 20 23:53:23 2021

@author: matte
"""

import folium 


def color_map_display(color_for_each_area, all_area_data, areas_names_list, myMap) :
    """Display the final color for each area of the map.
    
    :param color_for_each_area: The list of (str) color for every area.
    :type color_for_each_area: list
    :param all_area_data: The list that contain every information from the areas.
    :type all_area_data: list
    :param areas_names: The list of (str) names for each area.
    :type areas_names: list
    :param myMap: The folium map
    :type myMap: folium.folium.map
    :returns: Nothing, just display directly the colored areas on the map using folium
    """
    area_color = lambda x: { 'fillColor': x["geometry"]["color"],
             'fillOpacity' : 0.4,
             'color' : "#363636",
             'opacity' : 1                    
             }
    
    for index in range(len(color_for_each_area)):

        all_area_data[index]["index"]=index
        all_area_data[index]["color"]=color_for_each_area[index]

        folium.GeoJson(all_area_data[index], name=str(areas_names_list[index]),style_function=area_color).add_to(myMap)
    