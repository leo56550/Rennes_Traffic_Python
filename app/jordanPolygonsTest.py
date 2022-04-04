# -*- coding: utf-8 -*-
"""
Created on Sat Jun 19 17:30:24 2021

@author: matte
"""

#TEST FONCTION JORDAN


import jordanFunctionTest as jordan

point_coord_1= [ 0,0 ]
point_coord_2= [ 5,0 ]

poly_1= [ [-1,-1], [-1, 1], [ 1, 1], [1, -1 ] ]

if jordan.is_point_in_poly(point_coord_1, poly_1)==True:
   print("test ok point 1")

if jordan.is_point_in_poly(point_coord_2, poly_1) == False:
    print("test ok point 2")


poly_2= [ [0,0], [2, 1], [ 0, 2] ]
point_coord_1= [ 1,1 ]
point_coord_2= [ 5,0 ]

if jordan.is_point_in_poly(point_coord_1, poly_2)==True:
   print("test ok point 1.2")

if jordan.is_point_in_poly(point_coord_2, poly_2) == False:
    print("test ok point 2.2")


poly_3 = [ [0,0], [10, 0], [10, -10.], [0, -10], [0,-8], [2,-8], [2,-6],[0,-6],[0,0] ]
point_coord_1= [ -3,3 ]
point_coord_2= [ -50,0 ]
point_coord_3 = [-7,1]
if jordan.is_point_in_poly(point_coord_1, poly_3)==True:
   print("test ok point 1.3")

if jordan.is_point_in_poly(point_coord_2, poly_3) == False:
    print("test ok point 2.3")

if jordan.is_point_in_poly(point_coord_3, poly_3) == False:
    print("test ok point 3.1")
    
poly_4 = [ [0,0], [6, 0], [6, 10.], [0, 0] ]
point_coord_1= [ 1,5 ]
point_coord_2= [ 0,6 ]

if jordan.is_point_in_poly(point_coord_1, poly_4)==True:
   print("test ok point 1.4")

if jordan.is_point_in_poly(point_coord_2, poly_4) == False:
    print("test ok point 2.4")
