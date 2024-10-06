## PERIHELION  Mercury's perihelion precession and general relativity
#
# In this lab assignment, a student completes a Python program to test with
# data an accurate prediction of Einstein’s theory, namely the perihelion
# precession of Mercury. Mercury’s orbit around the Sun is not a stationary
# ellipse, as Newton’s theory predicts when there are no other bodies. With
# Einstein’s theory, the relative angle of Mercury’s perihelion (position
# nearest the Sun) varies by about 575.31 arcseconds per century.
#
# Copyright (c) 2022, University of Alberta
# Electrical and Computer Engineering
# All rights reserved.
#
# Student name: Huzaifa Asim
# Student CCID:
# Others:
#
# To avoid plagiarism, list the names of persons, Version 0 author(s)
# excluded, whose code, words, ideas, or data you used. To avoid
# cheating, list the names of persons, excluding the ENCMP 100 lab
# instructor and TAs, who gave you compositional assistance.
#
# After each name, including your own name, enter in parentheses an
# estimate of the person's contributions in percent. Without these
# numbers, adding to 100%, follow-up questions will be asked.
#
# For anonymous sources, enter pseudonyms in uppercase, e.g., SAURON,
# followed by percentages as above. Email a link to or a copy of the
# source to the lab instructor before the assignment is due.
#
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt

def main():
    data = loaddata('horizons_results')
    data = locate(data) # Perihelia
    data = select(data,25,('Jan','Feb','Mar'))
    makeplot(data,'horizons_results')

def loaddata(filename):
    """
    Load the data from a text file.

    Args:
    filename (str): Name of the file (without extension) to load.

    Returns:
    list: List containing dictionaries with numeric date, string date, and 3D coordinates.
    """
    file = open(filename+'.txt','r') #This opens the file in order to read it
    lines = file.readlines()
    file.close()
    noSOE = True # Indicates of the start of the data section has been reached
    num = 0 #No. of lines read
    data = [] #Stores the data that was loaded
    for line in lines:
        if noSOE:
            if line.rstrip() == "$$SOE": #To check if the start of a data section hass been reached
                noSOE = False # Set the indicator to false as start of data is reached
        elif line.rstrip() != "$$EOE": #Check if the end of the data is actually reached
            num = num+1 #Increment the number of lines that have been read
            if num % 10000 == 0:
                print(filename,":",num,"line(s)") #Print the progress for every 10k lines
            datum = str2dict(line) #Convert lines of text into a dictionary
            data.append(datum) #Add the dictionary to the list of data
        else:
            break # Exit the for loop in end of data reached
    if noSOE:
        print(filename,": no $$SOE line") #If the start cannot be found
    else:
        print(filename,":",num,"line(s)") #No. of lines
    return data #Return the data loaded

def str2dict(line):
    """
    Converting a line of text in to a dictionary.

    Args:
        line (str): The line of text that going to be converted.

    Returns:
        dict: A dictionary containing the converted data.
    """
    parts = line.split(',')  # Split the line
    numdate = int(float(parts[0]))  # Convert the first part to floating pt number then the 2nd part to an int
    strdate = parts[1][6:17]  # Get the date string from the second part
    coord = tuple(map(float, parts[2:-1]))  # Convert the remaining parts of it
    return {'numdate': numdate, 'strdate': strdate, 'coord': coord}  # Return a dictionary with the converted data


def locate(data1):
    """
    Locate the perihelia in the given data.

    Args:
        data1 (list): The data that is inputted.

    Returns:
        list: A list of dictionaries that contain the located perihelia.
    """
    dist = [] # Vector lengths
    for datum in data1:
        coord = np.array(datum['coord']) #Converts the coordinate tuple into a numpy array
        dot = np.dot(coord,coord) #Calculates dot product
        dist.append(np.sqrt(dot)) #For calculating vector length and add to list
    data2 = [] #Stores the located perihelia
    for k in range(1,len(dist)-1):
        if dist[k] < dist[k-1] and dist[k] < dist[k+1]: #In order to check if the current distance is lower than the next and last
            data2.append(data1[k])
    return data2 #Return located perihelia

def select(data,ystep,month):
    """
    Selecting the data based on the year and the month.

    Args:
        data: The inputted data.
        ystep: The year step.
        month: The months be selected.

    Returns:
        list: A list of dictionaries that contain the selected data.
    """
    dataSelected = []  # List to store the selected data
    for datum in data:
        year = int((datum['strdate'].split('-')[0])[0:4])  # Get the year from the string that contains the data
        monthStr = datum['strdate'].split('-')[1]  # Get the month from the string that contains the data
        if year % ystep == 0 and monthStr in month:  # Check if the year is a factor of ystep and the month is present in the list specified
            dataSelected.append(datum)  # In the selected list add the datum
    return dataSelected  # Return the selected data

def makeplot(data,filename):
    """
    Making a plot of the data.

    Args:
        data (list): The inputted data.
        filename (str): The name of the output file.
    """
    (numdate, strdate, arcsec) = precess(data)  # Calculating the precession angles
    plt.plot(numdate, arcsec, 'bo')  # Plotting the precession angles
    strdate = [datum['strdate'] for datum in data]  # Get the date strings from the data
    plt.xticks(numdate, strdate, rotation=45)  # Set the x-axis to the date strings
    add2plot(numdate, arcsec)  # Add a line of best-fit
    plt.xlabel('Perihelion date')  # x-axis label
    plt.ylabel('Precession (arcsec)')  # y-axis label
    plt.savefig(filename+'.png', bbox_inches='tight')  # Save the plot to a file
    plt.show()  # Show the plot

def precess(data):
    numdate = [] #A list that stores the numerical dates
    strdate = [] #A list that holds the date strings
    arcsec = [] #A list that holds the precession angles
    v = np.array(data[0]['coord']) # Reference (3D)
    for datum in data:
        u = np.array(datum['coord']) # Perihelion (3D)
        ratio = np.dot(u,v)/np.sqrt(np.dot(u,u)*np.dot(v,v)) #dot product ratio
        if np.abs(ratio) <= 1: #check ratio rangee
            angle = 3600*np.degrees(np.arccos(ratio)) #Calculate precession angle in units of angle in arcseconds
            numdate.append(datum['numdate']) #Add numerical date to list
            strdate.append(datum['strdate']) #Add the date to string list
            arcsec.append(angle) #Add precession angle to list
    return (numdate,strdate,arcsec)

def add2plot(numdate,actual):
    r = stats.linregress(numdate,actual) #perform linear regression
    bestfit = [] #hold best fit line
    for k in range(len(numdate)):
        bestfit.append(r[0]*numdate[k]+r[1]) #calculating the best fit line values
    plt.plot(numdate,bestfit,'b-') #plot the line of best fit
    plt.legend(["Actual data","Best fit line"]) #Include a legned 

#Start the program
main()
