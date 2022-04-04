# -*- coding: utf-8 -*-
"""
Created on Fri Jun 18 16:26:41 2021

@author: leobu
"""
from  flask  import  Flask , render_template, request 
import folium 
import Main_Program 
 
 
#application = Flask('traffic_rennes') 
application = Flask('Rennes Traffic') 
 
@application.route('/') 
def  index (): 
    print("je suis dans l'index") 
    return  render_template('index.html') 
 
@application.route('/display -map -static ') 
def  display_map_static (): 
    folium_map = folium.Map(location =[48.40701 ,  -4.49559]) 
    folium_map.save("templates/my_map.html") 
    return  render_template('my_map.html') 
 
@application.route('/display -map', methods=['GET'] ) 
def  display_map (): 
    nbpoints = request.args.get('nbpoints') 
    display_points = request.args.get('display_points') 
 
    if display_points == "1": 
        display_points = True 
    else: 
        display_points = False 
 
    is_online = request.args.get('is_online') 
    if is_online == "1":  
            local_API_name = '' 
            is_online=True 
    else:  
        local_API_name = request.args.get('local_API_name') 
        is_online=False 
 
 
    Main_Program.entry(is_online, display_points, nbpoints, local_API_name) 
     
    return  render_template("Rennes_Traffic_Map.html") 
     
 
print("launching app...") 
application.run(debug=True , threaded =True, use_reloader=False) 
     
print("App started.") 

