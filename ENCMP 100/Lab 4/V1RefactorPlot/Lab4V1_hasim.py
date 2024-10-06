## TSPANALYZE  Geomatics and the Travelling Sales[person] Problem
#
# According to the ISO/TC 211, geomatics is the "discipline concerned
# with the collection, distribution, storage, analysis, processing, [and]
# presentation of geographic data or geographic information." Geomatics
# is associated with the travelling salesman problem (TSP), a fundamental
# computing problem. In this lab assignment, a University of Alberta
# student completes a Python program to analyze, process, and present
# entries, stored in a binary data file, of the TSPLIB, a database
# collected and distributed by the University of Heidelberg.
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
#Import the module scipy.io
import scipy.io as io  
#Import matplotlib.pyplot
import matplotlib.pyplot as plt
#Import numpy  
import numpy as np  

def plot_2d_euclidean(coordinates, description, plot_name):
    """
    Function that plots 2D Euclidean coordinates.

    Parameters:
    - coordinates: numpy array of shape (N, 2) representing the x and y coordinates
    - description: string representing the plot description
    - plot_name: string representing the plot name
    """
    x_coords = coordinates[:, 0]  #Get the x-coordinates from the coordinates array
    y_coords = coordinates[:, 1]  #Get the y-coordinates from the coordinates array
    plt.plot(x_coords, y_coords, 'bo-')  #Plotting the coordinates by dots connecting them by lines (blue)
    plt.plot([x_coords[0], x_coords[-1]], [y_coords[0], y_coords[-1]], 'r-')  #Plot a red line that connects the first and last plot
    plt.xlabel('x-Coordinate')  #Setting the horizontal axis label
    plt.ylabel('y-Coordinate')  #Setting the veritcal axis label
    plt.title(description)  #Setting the title of the plot
    plt.savefig('tspPlot.png')  #Save the plot as image
    plt.legend([plot_name], loc='upper right')  #Add legend
    plt.show()  #Display the plot

def print_tsp_info(tsp_data):

    """
    Function that prints information about TSP data

    Parameters:
    - tsp_data: list of lists representing TSP data
    """
    print()

    print("NUM  FILE NAME  EDGE TYPE  DIMENSION  COMMENT")

    for k in range(1, len(tsp_data)):

        name = tsp_data[k][0]  #Get file name from TSP data
        edge = tsp_data[k][5]  #Get edge type from TSP data
        dimension = tsp_data[k][3]  #Get the dimension from TSP data
        comment = tsp_data[k][2]  #Get the comment from TSP data

        print("%3d  %-9.9s  %-9.9s  %9d  %s"
              
              % (k, name, edge, dimension, comment))  #Print info

def plot_tsp(tsp_data):
    """
    Function that plots a tour using data from TSP data.

    Parameters:
    - tsp_data: list of lists that represent the TSP data
    """
    tour_number = int(input("Number (EUC_2D)? "))  #Getting user input for the number of the tour
    tsp_tour = tsp_data[tour_number]  #Select tour 
    edge_type = tsp_tour[5]  #Get edge type
    if edge_type == 'EUC_2D':  #Check if the edge type is 'EUC_2D'

        print("Valid (%s)!!!" % edge_type)  #Print a validation message

        plot_2d_euclidean(tsp_tour[10], tsp_tour[2], tsp_tour[0])  #Plot tour by using the plot_2d_euclidean def
    else:
        print("Invalid (%s)!!!" % edge_type)  #Print an invalid message

def display_menu():
    """
    Function that displays the main menu and gets the user's choice.

    Parameters:
    No Parameters

    Returns:
    - choice: integer that is the the user's choice
    """
    print()
    print("MAIN MENU")
    print("0. Exit program")
    print("1. Print database")
    print("2. Limit dimension")
    print("3. Plot one tour")

    choice = int(input("Choice (0-3)? "))  #Getting user input for their choice

    while not (0 <= choice <= 3):  #Validate the user choice
        choice = int(input("Choice (0-3)? "))  #Get the users input again if the choice is not one thats valid
    return choice  #Return the user's choice

def main():

    tsp_data = io.loadmat('tspData.mat', squeeze_me = True)
    tsp_data = np.ndarray.tolist(tsp_data['tsp'])  #Convert to list of lists
    file = open('tspAbout.txt', 'r')  #Open tspAbout.txt
    print(file.read())  #Print the contents of the file

    file.close()  #Close

    choice = display_menu()  #Get the user's choice from the menu
    while choice != 0:  #Loop until exit

        if choice == 1:  #run first def
            print_tsp_info(tsp_data)

        elif choice == 3:  #run third def
            plot_tsp(tsp_data)

        choice = display_menu()  #Get options again

if __name__ == "__main__":    
    main() 