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
# numbers, adding to 100%, follow-up questions may be asked.
#
# For anonymous sources, enter pseudonyms in uppercase, e.g., SAURON,
# followed by percentages as above. Email a link to or a copy of the
# source to the lab instructor before the assignment is due.
#
import matplotlib.pyplot as plt
import numpy as np

print('Version 2')
# ------------Students edit/write their code below here--------------------------
# ------------Remove any code that is unnecessary--------------------------

# Calculate Savings

# Total Months
numMonths = 18 * 12
# Contribution
monthlyContributions = 200
# Interest Rate
rateInterest = 0.0625
# Declare the old balance (initial value)
oldBalance = 2000
# Create a list that stores the monthly balances
monthlyBalance = [oldBalance]
# New balance
newBalance = 0

# Calculate the Monthly Balances + interest
for i in range(1 , numMonths):
    newBalance = oldBalance * (1 + rateInterest / 12) + monthlyContributions
    monthlyBalance.append(newBalance)
    oldBalance = newBalance
    
# Print the value of the Savings after the Number of Months elapses
print(f"The savings amount is ${monthlyBalance[-1]:.2f}")

# Calculating the Tuition

# Create a list to hold the tuition cost for Arts
arts = [5550]
# Create a list to hold the tuition cost for Science
science = [6150]
# Create a list to hold the tuition cost for Engineering
engineering = [6550]
# The rate at which the tuition costs increase
rateIncrease = 7/100

# Calculating the cost of tuition for 22 years
for i in range(1, 22):
    arts.append(arts[-1] * (1 + rateIncrease))
    science.append(science[-1] * (1 + rateIncrease))
    engineering.append(engineering[-1] * (1 + rateIncrease))
    
# The cost of tuition for each faculty over 4 years
artsFourYears = sum(arts[-4:])
scienceFourYears = sum(science[-4:])
engineeringFourYears = sum(engineering[-4:])

# Print the cost of each faculty for four years to the console
print(f"The cost of the arts program is ${artsFourYears:.2f}")
print(f"The cost of the science program is ${scienceFourYears:.2f}")
print(f"The cost of the engg program is ${engineeringFourYears:.2f}")

# Plot the Data

# x-axis
xValues = np.arange(19)  # Extend the range to include age 18
# y-axis
yValues = [monthlyBalance[12 * i]
            for i in range(18)]
# Increase the range so it has the final balance
yValues.append(monthlyBalance[-1])
# Plot the amount in the Savings
plt.plot(xValues, yValues, label = 'Saving Balance')
# Plot the lines for the tuition prices
plt.axhline(y = scienceFourYears, color = 'green', label = 'Science')
plt.axhline(y = artsFourYears, color = 'orange', label = 'Arts')
plt.axhline(y = engineeringFourYears, color = 'red', label = 'Engineering')
# Making a title, labels and a legend for the graph
plt.title('Savings vs Tuition')
# Axis titles and increments
plt.xlabel('Years')
plt.ylabel('Amount $')
plt.xticks(np.arange(0, 19, 1))
# Domain and Range
plt.ylim(0, 100000)
plt.xlim(0, 18)
#Legend
plt.legend()
# Print the plot
plt.show()

# Version 2

# Ask the user to input their choice of program
programSelect = int(input("Enter a program, 1. Arts, 2. Science, 3. Engineering: "))

# Define a function that calculates the optimal monthly contribution
def optimalContribution(costOfTuition):
    # Total Months
    numMonths = 18 * 12
    # Contribution
    monthlyContributions = 1
    # Interest Rate
    rateInterest = 0.0625
    # Declare the old balance (initial value)
    oldBalance = 2000
    # Create a list that stores the monthly balances
    monthlyBalance = [oldBalance]
    # Optimized Balanced
    newOptimizedBalance = 0
    
    while newOptimizedBalance < costOfTuition:
        monthlyContributions += 1
        # Reset the old balance back to two thousand
        oldBalance = 2000
        # Now calculate the monthly balances
        for i in range(1, numMonths):
            newOptimizedBalance = oldBalance * \
                (1 + rateInterest / 12) + monthlyContributions
            monthlyBalance.append(newOptimizedBalance)
            oldBalance = newOptimizedBalance
            
    print(f"The optimal monthly contribution amount is ${monthlyContributions}")
    
# Doing the calculations based on the selected program:
if programSelect == 1:
    
    if monthlyBalance[-1] >= artsFourYears:
        print("Congratulations! You have saved enough for the arts program.")
    
    else:
        print("Unfortunately you do not have enough saved for the arts program.")
    optimalContribution(artsFourYears)

elif programSelect == 2:
    
    if monthlyBalance[-1] >= scienceFourYears:
        print("Congratulations! You have saved enough for the science program.")
    
    else:
        print("Unfortunately you do not have enough saved for the science program.")
    optimalContribution(scienceFourYears)

elif programSelect == 3:
    
    if monthlyBalance[-1] >= engineeringFourYears:
        print("Congratulations! You have saved enough for the engineering program.")
    
    else:
        print("Unfortunately you do not have enough saved for the engineering program.")
    optimalContribution(engineeringFourYears)