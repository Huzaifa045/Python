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

import numpy as np
print('Version 2')
# ----------Students write/modify their code below here ---------------------
code = input('Please enter a code to break: ')
code = np.array(list(code),dtype=int)

# Version 1 will implement Rules 1 and 2. Rules 3 and 4 will be implemented partially

# Implement Rule 1
# Valid code must be 9-digits
if len(code) != 9:
    print("Decoy Message: Not a nine-digit number") 
    
# Implement Rule 2
# Even sum of digits is invalid. Program will continue if the sum of digits is odd.
elif sum(code) % 2 == 0:
    print("Decoy Message: Sum is Even.")
    
else:
# Implement Rule 3
# Multiply the 3rd digit by the 2nd digit and subtract the 1st digit
     # Setting the variable rescued = True. Will allow for running rule 4.
    rescued = True
    ruleThree = (code[2] * code[1]) - code[0]
    # Assign a number to each possible resuce day
    if ruleThree == 1:
        rescueDay = "Monday"
    elif ruleThree == 2:
        rescueDay = "Tuesday"
    elif ruleThree == 3:
        rescueDay = "Wednesday"
    elif ruleThree == 4:
        rescueDay = "Thursday"
    elif ruleThree == 5:
        rescueDay = "Friday"
    elif ruleThree == 6:
        rescueDay = "Saturday"
    elif ruleThree == 7:
        rescueDay = "Sunday"
    else:
        # If the expression does not output a number 1-7 then it is invalid.
        print("Decoy Message: Invalid Rescue Day")
        rescued = False
        
# Implement Rule 4
# Take the 3rd digit to the power of the 2nd.
    if rescued:
        ruleFour = code[2]**code[1]
        # if there is no remainder after dividing by 3 subtract 6th digit from 5th digit
        if ruleFour % 3 == 0: 
            numFour = code[5] - code[4]
            #if there is remainder after dividing by 3 subtract 5th digit from 6th
        else: 
            numFour = code[4] - code[5]   
            # Assign a number to each rendezvous/rescue point
        if numFour == 1:
                rescueLocation = "bridge"
        elif numFour == 2:
                rescueLocation = "library"
        elif numFour == 3:
                rescueLocation = "river crossing"
        elif numFour == 4:
                rescueLocation = "airport"
        elif numFour == 5:
                rescueLocation = "bus terminal"
        elif numFour == 6:
                rescueLocation = "hospital"
        elif numFour == 7:
                rescueLocation = "railway station"
                # If the result is none of the numbers 1-7 it is invalid
        else:
            print("Decoy Message: Invalid rendezvous point")
                
    
            rescued = False  
                
    if rescued:
        # Print the day and location of the rescue
            print("Rescued on", rescueDay, "at the", rescueLocation)
        
        
        
        
        

        
        
        
