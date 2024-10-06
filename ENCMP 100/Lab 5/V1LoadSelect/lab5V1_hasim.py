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
# Student name: 
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
import csv
import matplotlib.pyplot as plt

def main():
    data = loaddata('horizons_results')
    data = locate(data) # Perihelia
    data = select(data, 50 ,('Jan','Feb','Mar')) #Edited to select perihelia at half-century intervals
    data = refine(data, 'horizons_results')  # Refine the data immediately after the select invocation
    makeplot(data, 'horizons_results')  # Make a plot of the data
    savedata(data, 'horizons_results')  # Save the selected data to a file

def refine(data, filename):
    """
    Refining by loading additional files and loacting the perihelia.
    Args:
        data: The inputted data.
        filename: The base name of the files to be loaded.
    Returns:
        list: A list of dictionaries containing the initial perihelion of each loaded file.
    """
    refinedData = []  # Store the refined data list
    for datum in data:
        suffix = datum['strdate']  # Extract the suffix from the 'strdate' of each dictionary entry
        fileToLoad = filename + '_' + suffix + '.txt'  # Compose the file name for loading
        loadedData = loaddata(fileToLoad)  # Load the additional file
        perihelion = locate(loadedData)[0]  # Find the first perihelion in the loaded data
        refinedData.append(perihelion)  # Append the perihelion to the refined data list
    return refinedData  # Provide the refined data

def savedata(data, filename):
    """
    Store the selected data in a CSV file.
    Args:
        data (list): The data to store.
        filename (str): The name of the output file.
    """
    filename += '.csv'  # Append the .csv extension if missing
    with open(filename, 'w', newline='') as file:
        writer = csv.writer(file)
        
        # Compose the header
        writer.writerow(["NUMDATE","STRDATE","XCOORD","YCOORD","ZCOORD"])
        
        # Store the data
        for datum in data:

            numdate = datum['numdate']  # Extract the numerical date from the datum dictionary
            strdate = datum['strdate']  # Extract the date string from the datum dictionary
            coord = ','.join(map(str, datum['coord']))  # Convert the coordinate tuple to a comma-separated string
            xcoord, ycoord, zcoord = map(float, coord.split(','))  # Split the coordinate string and convert each part to a float
            writer.writerow([format(numdate, '.6f'), strdate, format(xcoord, '.6f'), format(ycoord, '.6f'), format(zcoord, '.6f')])  # Store the refined data in the CSV file

def loaddata(filename):
    """
    Retrieve the data from the text file.

    Args:
        filename: The name of the file to get the data from.

    Returns:
        list: A list of dictionaries that contain that retrieved data
    """
    if filename == 'horizons_results':
        
        filename = filename + '.txt'  # Ensure the file extension is included if absent
    file = open(filename,'r')  # Open the file for reading
    lines = file.readlines()  # Read all lines from the file
    file.close()  # Close the file
    noSOE = True  # Flag indicating if the start of the data section has been encountered
    numb = 0  # Counter for the number of lines read
    dataReturned = []  # List to store the retrieved data
    for line in lines:
        if noSOE:
            if line.rstrip() == "$$SOE":  # Check if the start of the data section has been reached
                noSOE = False  # Set the flag to false to indicate the start of the data section
        elif line.rstrip() != "$$EOE":  # Check if the end of the data section has been reached
            numb = numb+1  # Increment the line counter
            if numb % 10000 == 0:
                print(filename,":",numb,"line(s)")  # Display progress every 10000 lines
            datum = str2dict(line)  # Convert the line of text into a dictionary
            dataReturned.append(datum)  # Add the dictionary to the data list
        else:
            break  # Exit the loop if the end of the data section is encountered
    if noSOE:
        print(filename,": no $$SOE line")  # Print a message if the start of the data section is not found
    else:
        print(filename,":",numb,"line(s)")  # Display the total number of lines read
    return dataReturned  #Return the loaded data

def str2dict(line):
    """
    Converting a line of text in to a dictionary.

    Args:
        line: The line of text that going to be converted.

    Returns:
        dict: A dictionary containing the converted data.
    """
    parts = line.split(',')  # Split the line
    numdate = int(float(parts[0]))  # Convert the first part to floating pt number then the 2nd part to an int
    strdate = parts[1][6:17]  # Get the date string from the second part
    coord = tuple(map(float, parts[2:-1]))  # Convert the remaining parts of it
    return {'numdate': numdate, 'strdate': strdate, 'coord': coord}  # Return a dictionary with the converted data


def locate(inData):
    """
    Locate the perihelia in the given data.

    Args:
        inData: The data that is inputted.

    Returns:
        list: A list of dictionaries that contain the located perihelia.
    """
    dist = [] # Vector lengths
    for datum in inData:
        coord = np.array(datum['coord']) #Converts the coordinate tuple to a numpy array
        dot = np.dot(coord,coord) #Calculating the dot product
        dist.append(np.sqrt(dot)) #For calculating vector length and adding it to the list
    data = [] #Stores the located perihelia
    for k in range(1,len(dist)-1):
        if dist[k] < dist[k-1] and dist[k] < dist[k+1]: #In order to check if the current distance is lower than the next and last
            data.append(inData[k])
    return data #Return located perihelia

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
        data: The inputted data.
        filename: The name of the output file.
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
        ratio = np.dot(u,v)/np.sqrt(np.dot(u,u)*np.dot(v,v)) #the dot product ratio
        if np.abs(ratio) <= 1: #check ratio ranges
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
    slope = r[0] * 365.25 * 100 #Slope in units of arcsecs per day
    plt.title(f"Slope of the best fit line: {slope:.2f} arcsec/cent") # The title of the plot and the slope of the line of best fit
    plt.legend(["Actual data", f"Best fit line"], loc="upper left") #Include a legned 

#Calling the main function
main()