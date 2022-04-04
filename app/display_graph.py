# -*- coding: utf-8 -*-
"""
Created on Tue Jun 22 16:10:03 2021

@author: matte
"""

import matplotlib.pyplot as plt
import json
import os 
import numpy as np


###############################
#Functions 
###############################    

def get_historical_data(data_file_name) :
    """Get the data from the all the API files in the folder 'historical_data'
    
    :param data_file_name: The list of names for all the API files in the folder.
    :type data_file_name: list
    :return: Lists of traffic status and dates (Y-month-day).
    :rtype: list
    """
    big_list =[]
    traffic_data_list = []
    short_date_list = []
    full_date_list = []
    for name in data_file_name : 
        
       big_list.append(json.load(open("historical_data/"+ str(name))))  #we open each API file one after the other
       
    for file in big_list :      
        traffic_data_temp = 4
        temp_date = []        #we creat temporary variables 
        for i in range(len(file["records"])) :
            temp_date.append(file["records"][1]["fields"]['datetime'][0:10])   #Get the first point date for each file
            
            if file["records"][i]["fields"]["trafficstatus"] == "impossible" :  #Append the "most bad" status, so if a lowest value is found in the file, we replace the others 
                traffic_data_temp=(1)                                           #Also replace the str by an int, easier to put on a graph
            if file["records"][i]["fields"]["trafficstatus"] == "congested" :
                if traffic_data_temp >= 2:
                    traffic_data_temp=(2)
            if file["records"][i]["fields"]["trafficstatus"] == "heavy" :
                if traffic_data_temp >= 3:
                    traffic_data_temp=(3)
            if file["records"][i]["fields"]["trafficstatus"] == "freeFlow" :
                if traffic_data_temp >= 3:
                    traffic_data_temp=(4)
        
        full_date_list.append(temp_date)       #we append the principal list with the temp list in order to have a list of list.
        traffic_data_list.append(traffic_data_temp)
        
    for date in (full_date_list) :         #for every date we simplify it to only keep the Year-Month-Date 
            short_date_list.append(date[0])
            
    return traffic_data_list, short_date_list

#--------------------------------------------------------------------------------------------------------------------

def separate_categories(traffic_data, dates_list) : 
    """Separate every traffic point into categories lists
    
    :param traffic_data: The list of numbers that represent the status for each file.
    :type traffic_data: list
    :param dates_list: The list of dates for each file.
    :type dates_list: list
    :return: 8 lists, date and status for the 4 possibilities.
    :rtype: list
    """

    freeflowlist = []
    heavyList = []
    congestedList = []
    impossibleList = []
    
    date_freeflowlist = []
    date_heavyList = []
    date_congestedList = []
    date_impossibleList = []
    
    for data in range(len(traffic_data)) :       #Divide every point in its new category list
        if traffic_data[data] == 4 : 
            freeflowlist.append(traffic_data[data])
            date_freeflowlist.append(data)
        if traffic_data[data] == 3 : 
            heavyList.append(traffic_data[data])
            date_heavyList.append(data)
        if traffic_data[data] == 2 : 
            congestedList.append(traffic_data[data])
            date_congestedList.append(data)
        if traffic_data[data] == 1 : 
            impossibleList.append(traffic_data[data])
            date_impossibleList.append(data)
            
    return freeflowlist, date_freeflowlist, heavyList, date_heavyList, congestedList, date_congestedList, impossibleList, date_impossibleList
        
#--------------------------------------------------------------------------------------------------------------------
    
def graph_creation() :
    """Creates the graph and a .png file in the static folder
    
    :return: Nothing, display the graph and creates an image.png in the static folder.
    """
    data__files_names_list = os.listdir('historical_data/')
    
    traffic_data, dates_list = get_historical_data(data__files_names_list)  #Run the upper functions
    
    
    freeflowPoints, date_freeflow, heavyPoints, date_heavy, congestedPoints, date_congested, impossiblePoints, date_impossible = separate_categories(traffic_data, dates_list)
    
    
    fig = plt.figure()           #Create the figure
    fig.set_size_inches(18, 4)   #Set the size for a better result 
    
    ax = fig.add_subplot (1,1,1) 
    ax.scatter (date_freeflow, freeflowPoints, color = 'g', label = "FreeFlow")     #One for each status
    ax.scatter (date_heavy, heavyPoints, color = 'orange', label = "Heavy")
    ax.scatter (date_congested, congestedPoints, color = 'r', label = "Congested") 
    ax.scatter (date_impossible, impossiblePoints, color = 'black', label = "Impossible")
    
    Xaxis_tick = []    #We change the nammes of the axis values for a better understanding
    for date in dates_list :
        while date not in Xaxis_tick:   # Only pick differents dates
            Xaxis_tick.append(date)
    Yaxis_tick = ["Impossible","Congested", "Heavy", "FreeFlow"]  
    
    ax.set_xticklabels(Xaxis_tick)
    ax.set_yticklabels(Yaxis_tick)      #Thess part of the code are adapted from a Stackoverflow articles about matplotlib and custom axis
    plt.yticks(np.arange(1, 5, 1))   
    
    ax.legend(loc = "upper right", bbox_to_anchor=(1,0.9))   
    ax.grid()
    ax.set (xlabel = "Date", ylabel = "Traffic Status", title = "Rennes's road traffic for 7 days")
    
    fig.savefig('static/Rennes_historical_traffic.png', dpi=400)


     
###############################
#Program Launch
###############################    

graph_creation()    
    
    
    


