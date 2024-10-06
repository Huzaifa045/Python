

import scipy.io as sio  # Utilizing the scipy.io library for file operations

import matplotlib.pyplot as plt  # Incorporating matplotlib.pyplot for plotting

import numpy as np  # Importing numpy for numerical functions

 

 

 

 

def plotEuc2D(coord, comment, name):

    """

    Displays 2D Euclidean coordinates.

 

    Parameters:

    - coord: NumPy array of shape (N, 2) containing x and y coordinates

    - comment: Descriptive string for the plot

    - name: Name of the plot

    """

    x = coord[:, 0]  # taking x coordinates from the array

    y = coord[:, 1]  # taking y coordinates from the array

    plt.plot(x, y, 'bo-')  # making the plot dots blue, connecting with a stright lines

    plt.plot([x[0], x[-1]], [y[0], y[-1]], 'r-')  # computing red line between the first and last points

    #setting labels

    plt.xlabel('x-Coordinate') 

    plt.ylabel('y-Coordinate')

    plt.title(comment)  # Sets the plot title

    plt.savefig('tspPlot.png')  # Saves the plot as an image file

    plt.legend([name], loc='upper right')  # this function is used too add a legend to the plot

    plt.show()

 

 

 

def tspPrint(tsp):

    """

    Function to print information about the TSP data.

 

    Parameters:

    - tsp: List of lists representing the TSP data

    """

    print()

    print("NUM  FILE NAME  EDGE TYPE  DIMENSION  COMMENT")

    for k in range(1, len(tsp)):

        name, edge, dimension, comment = tsp[k][0], tsp[k][5], tsp[k][3], tsp[k][2]

        print("%3d  %-9.9s  %-9.9s  %9d  %s" % (k, name, edge, dimension, comment))

 

 

def tspPlot(tsp):

    """

    this allows me too plot the jounrry on a graph

    

    Parameters:

    list of lists representing the TSP data

    """

    # ths is allowing us too obtain the user input for the number for the tour

 

    num = int(input("Number (EUC_2D)? ")) 

    while (num>1 and num>len(tsp)):

            num = int(input("Number (EUC_2D)? "))

            

    # onbtaining the edge type of the selected tour

    edge = tsp[num][5]

    if edge == 'EUC_2D':

        # Selecting the tour from the tsp data

        tsp1 = tsp[num] 

        print("Valid (%s)!!!" % edge)  # Printing a valid

        plotEuc2D(tsp1[10], tsp1[2], tsp1[0])  # Ploting tour

    else:

        print("Invalid (%s)!!!" % edge)  # Printing an invalid message

 

 

def menu():

    """

    Displays the main menu and obtains user choice.

 

    gives us:

    integer (1,2,or3) representing the user's choice

    """

    print()

    print("MAIN MENU")

    print("0. Exit program")

    print("1. Print database")

    print("2. Limit dimension")

    print("3. Plot one tour")

    print()

    choice = int(input("Choice (0-3)? "))  # is able too obtain user input for the choice

    while not (0 <= choice <= 3):  # Validates the choice

        choice = int(input("Choice (0-3)? "))  # Prompts the user for the choice to change again if invalid

    return choice  # this function returns the user's choice

 

 

 

def main():

    tsp = sio.loadmat('tspData.mat', squeeze_me=True)  # loading data

    tsp = np.ndarray.tolist(tsp['tsp'])  # Converting the data into a list of data

    file = open('tspAbout.txt', 'r') 

   

    # Printing file

    print(file.read()) 

    file.close() 

 

 

 

def tspLimit(tsp):

    """

    This function limits the dimension of the TSP data by removing records with a dimension greater than a specified limit.

 

    Parameters:

    the given parameter written as "tsp" in the tspLimit is a list of lists representing the TSP data

 

    """

    # Compute the minimum and maximum dimension of the TSP data

    min_dim, max_dim = tsp_min_max(tsp)

    print("Minimum dimension:", min_dim[0]) # Print the minimum value

    print("Maximum dimension:", max_dim[1]) # Print the maximum value

   

    # now we must allow the user too imput values for the limits

    limit = (int(input("Limit Value? ")))

   

    # we now have too determine if the imputed values from the user is outside the minimum and maximum 

    while limit > max_dim or limit < min_dim:

        limit = int(input("Please enter a limit value within the range {} to {}: ".format(min_dim, max_dim)))

   

    # Crearing new list:

    newTsp = [tsp[0]]

   

    for record in tsp[1:]:

        if int(record[3]) <= limit:

            newTsp.append(record)

   

    # Returning the filtered data

    return newTsp

 

def tsp_min_max(tsp):

    """

    this function "tsp_min_max" allows me to compute the min and max dimension of the data.

 

    Parameters:

    the given parameter written as "tsp" in the tsp_min_max is a list of lists representing the TSP data

 

    which shows the follwowing:

    minimal Value: integer representing the min dimension

    maximum Value: integer representing the max dimension

    """

    # storing the dimensions

    dimension = []

 

    # y utalizsing the append function we can append the dimension value to the dimensions list

    for i in range(1, len(tsp)):

        dimension.append(tsp[i][3])

 

    # Return the minimum and maximum dimension values

    return min(dimension), max(dimension)

 

 

 

    choice = menu()  # this function allows the user to imput their value from the menu 

    while choice != 0:  # this will allow loop until the user exits

        if choice == 1:  # this is if the user decides too print the data

             tspPrint(tsp)  # Call the tspPrint function to print the TSP data

        elif choice == 2:  # this is for if the user limites the dimensions

             tsp = tspLimit(tsp)  # Call the tspLimit function to limit the dimension of the TSP data

        elif choice == 3:  # this function is if the user decides to view the jounrey

             tspPlot(tsp)  # plotting the jounrney

 

        choice = menu()  # Getting the user's choice again from the menu

 

 

if __name__ == "__main__":

    main()  # Calls the main function