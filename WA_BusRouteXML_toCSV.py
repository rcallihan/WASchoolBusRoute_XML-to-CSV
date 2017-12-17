#This script is meant to handle transportation data from school districts in Washington. 
#Their systems will export (for state reporting purposes) bus route data into individual xml's per school. 
#this script will run through a directory of school xml's and return two csv's for each school: Bus Routes and Stop Assignment info. 

#Author: Ryan Callihan


from os import listdir
from os.path import isfile, join
import xml.etree.ElementTree as ET
import csv

def writeStudentAssignmentsToCSV(root,name):
    
    stopassignments_csv = name + '_stopassignments.csv'
    
    with open(stopassignments_csv, 'w') as csvfile: 
        
        csvfile.write('routeid, StopId, DestinationID, AssignedStudents\n')
        
        for Route in root.iter('Route'):
            routeid = Route.attrib['id']

            for sa in Route.iter('StudentAssignments'):
                StopId = (sa[0].text)
                DestinationID = (sa[1].text)
                AssignedStudents = (sa[2].text)
                line = "{},{},{},{}".format(routeid, StopId, DestinationID, AssignedStudents)

                csvfile.write(line)
                csvfile.write('\n')
                
    return stopassignments_csv
                
def writeRoutesToCSV(root, name):
    
    route_csv = name + '_routes.csv'
        
    with open(route_csv, 'w') as csvfile:
        
        csvfile.write('routeid, stopID, stopordinal,StopDescription, Latitude, Longitude\n')
        
        for Route in root.iter('Route'):
            routeid = Route.attrib['id']

            for stop in Route.iter('Stop'):
                stopID = stop.attrib['id']
                stopordinal = stop[0].text
                StopDescription = stop[1].text
                Latitude = stop[2].text
                Longitude = stop[3].text
                line = "{},{},{},{},{},{}".format(routeid, stopID, stopordinal,StopDescription, Latitude, Longitude)
                
                csvfile.write(line)
                csvfile.write('\n')
                
    return route_csv                     
            
            
for root, dirs, files in os.walk('.', topdown=True):
    dirs.clear() 
    for file in files:
        if ".xml" in file:

            tree = ET.parse(file)
            root = tree.getroot() 
            name = (file.split('.')[0])

            outputRoute = writeRoutesToCSV(root, name)
            outputAssingment = writeStudentAssignmentsToCSV(root, name)
            
            print("print {} --> {} {}".format(file, outputRoute, outputAssingment))