# -*- coding: utf-8 -*-
"""
Created on Sat Jun 19 16:22:53 2021

@author: matte
"""

def is_point_in_poly(coord_point,coord_polygon):
     
    nombre_sommets = len(coord_polygon)  
    inside = False  
    counter = 0
    p1x,p1y = coord_polygon[0]   
    i=0
    while i<nombre_sommets : 
        p2x,p2y = coord_polygon[i]
        if coord_point[0] > min(p1y,p2y) and coord_point[0] <= max(p1y,p2y) :   
                if coord_point[1] <= max(p1x,p2x):                             
                    if p1y != p2y :  
                         abscisseB = (p2x-p1x)*((p1y-coord_point[0])/(p1y-p2y))-(coord_point[1]-p1x) 
                    if p1x == p2x or coord_point[1] <= abscisseB:       
                        counter +=1     
        p1x,p1y = p2x,p2y
        i+=1
    if counter %2 != 0 : 
        inside = True
    
    return inside 