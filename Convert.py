
# coding: utf-8

# In[57]:


# Import necessary libraries, get setup
import pandas as pd
import numpy as np
from numpy import genfromtxt
import csv
import re


# In[28]:


regData = pd.read_excel('./RegistrationForm.xlsx')


# In[30]:


RegistrationInfo = regData[['Faculty_Advisor_Email','Name_of_School']].dropna()


# In[46]:


RegistrationInfo[0:3]


# In[51]:


RegistrationInfo.at[0,'Name_of_School']


# In[52]:


datafile = open('./output.csv', 'r')
datareader = csv.reader(datafile)


# In[53]:


def getEmail(school):
    for i in range(RegistrationInfo.shape[0]):
        if (RegistrationInfo.at[i,'Name_of_School']) == school:
            return RegistrationInfo.at[i,'Faculty_Advisor_Email']
    print('Cant find email for school: ' + school)
    return input("What is the email? ")
    
    
header = True
outputData = []
for row in datareader:
    if header is True:
        header = False
        continue
    school = row[0]
    email = getEmail(school)
    assignments = []
    for i in range(3,len(row)):
        assignments.append(row[i])
        
    outputData.append({
        'school': school,
        'email': email,
        'assignments': assignments
    })        


# In[56]:


outputData[0:1]


# In[ ]:


datafile = open('./AshtonCountryData.csv', 'r')
datareader = csv.reader(datafile)

countries = {}
for row in datareader:
    country = row[0]
    #if countries[country]:
    countries[country] = []
    for i in range(1,len(row)):
        countries[country].append(row[i])

datafile = open('./AshtonCharData.csv', 'r')
datareader = csv.reader(datafile)

characters = {}
for row in datareader:
    character = row[0]
    #if countries[country]:
    characters[character] = row[1]
    
    
totalColumns = 166
with open('import.csv','w') as fp:
    fp.write("Faculty_Advisor_Email,Name_of_School,.....,Remaining\n")
    for entry in outputData:    
        outputCSV = entry.email + ","
        for j in range(entry.assignments):
            assignment = entry.assignments[j]
            if re.match(r'.*\(\d+\)',assignment):
                # we are matching a country because they have format Country 1 (4)
                # our regex is .*(\d+) -> any characters, with a parentheses and one or more digits in the parentheses
                outputCSV += assignment + ","
                assignment = assignment.split('(')
                assignment = assignment[0].strip()
                committees = countries[assignment]
                commasToAdd = 10-(len(committees)%10)
                for i in range(len(committees)):
                    if i != 0 and (i+1)%10 == 0:
                        if (i+1) < len(committees):
                            outputCSV += committees[i] + "," + assignment + ","
                        else:
                            outputCSV += committees[i] + ","
                    else:
                        outputCSV += committees[i] + ","
                for i in range(commasToAdd):
                    outputCSV += ","
                
            else:
                outputCSV += 'Character Assignments'
                chars = entry.assignments[i:]
                for i in range(len(chars)):        
                    char = chars[i]
                    committee = characters[char]
                    
                    if i != 0 and (i+1)%10 == 0:
                        if (i+1) < len(chars):
                            outputCSV += chars[i] + ' (' + committee + ")," + 'Character Assignments,'
                        else:
                            outputCSV += chars[i] + ' (' + committee + "),"
                    else:
                        outputCSV += chars[i] + ' (' + committee + "),"
                break
                
        if outputCSV.endswith(','):
            outputCSV = outputCSV[:-1]
            
        outputArr = outputCSV.split(',')
        for i in range(len(outputArr),totalColumns):
            outputCSV += ','
            
        fp.write(outputCSV + "\n")
                        
            
    

