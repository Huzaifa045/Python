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

print('Version 1')
# ----------Students write/modify their code below here ---------------------
code = input('Please enter a code to break: ')
code = np.array(list(code),dtype=int)
print("The code entered is %s" % code)

# Version 1 will implement Rules 1 and 2. Rules 3 and 4 will be implemented partially

# Implement Rule 1
# Valid code must be 9-digits
if len(code) != 9:
    print("Decoy Message: Not a nine-digit number") 
    
# Implement Rule 2
# Even sum of digits is invalid
elif sum(code) % 2 == 0:
    print("Decoy Message: Sum is Even.")
    
else:
# Partially  Implement Rule 3
# Multiply the 3rd digit by the 2nd digit and subtract the 1st digit and print to console
    ruleThree = (code[2] * code[1]) - code[0]
    print("day =",ruleThree)

# Partially Implement Rule 4
# Take the 3rd digit to the power of the 2nd
ruleFour = code[2]**code[1]
if ruleFour % 3 == 0: # if there is no remainder after dividing by 3 subtract 6th digit from 5th
    print("place =",code[5] - code[4])
else: #if there is remainder after dividing by 3 subtract 5th digit from 6th
        print("place =",code[4] - code[5])
        
