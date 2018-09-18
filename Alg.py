
# coding: utf-8

# ### Country Automation
# 
# To do the country automation, a priority lottery will be utilized
# 
# #### Requirements
# 1. Pandas - python library
# 2. CSV of schools, delegate numbers, entries, countries, country positions, characters

# In[2]:


# Import necessary libraries, get setup
import pandas as pd
import numpy as np
from random import randint
from random import shuffle

data = pd.read_csv('./data.csv')
data[0:10]


# ### Setup school data: grab schools, delegates, entries and drop the NaN

# In[3]:


schools_arr = data[['Schools','Delegates','Entries']].dropna()
schools = []
for i in range(schools_arr.shape[0]):
    schools.append(
        {'school': str(schools_arr.at[i,'Schools']), 
         'delegates': int(schools_arr.at[i,'Delegates']),
         'entries': int(schools_arr.at[i,'Entries']),
         'remaining': int(schools_arr.at[i,'Delegates']),
         'countries': [], 'characters': []
        }
    )
schools[0:3]


# ### Setup country data: country name and position

# In[4]:


country_arr = data[['Countries','Positions']].dropna()
countries = []
for i in range(country_arr.shape[0]):
    countries.append({'country': str(country_arr.at[i,'Countries']),'positions': int(country_arr.at[i,'Positions'])})
countries[0:3]


# ### Setup character name: character name

# In[5]:


char_arr = data[['Characters']].dropna()
characters = []
for i in range(char_arr.shape[0]):
    characters.append({'character': str(char_arr.at[i,'Characters'])})
characters[0:3]


# ### Setup the priority 'hat'. Put several of each school name in the hat (determined by entry number)

# In[6]:


# Create the priority lottery array
school_priority_list = []
for entry in schools:
    school_priority_list += [entry['school']] * entry['entries']
shuffle(school_priority_list)
school_priority_list[0:3]


# ### Now, we have the data prepared; define some functions to check if we are done; first constants

# In[7]:


percentageCountry = 0.80
schoolsOnNextStage = []
assignAttemps = 25


# ### doneCountries() will determine if we are finished the country stage
# ### assignCountry() will assign a country to a school (the algorithm)
# ### findIndexOfSchool() will use schoolName to find school object in the schools array
# ### removeFromPriority() will remove all the entries of a school, once its has enough country assignments

# In[8]:


def doneCountries(currIteration,maxIterations):
    if currIteration >= maxIterations:
        return True
    if len(schools) == 0:
        return True
    if len(school_priority_list) == 0:
        return True
    if len(countries) == 0:
        return True
    return False

def assignCountry():
    country = countries[0]
    for i in range(assignAttemps):
        randInt = randint(0, len(school_priority_list) - 1) 
        schoolName = school_priority_list[randInt]
        ind = findIndexOfSchool(schoolName)
        if schools[ind]['remaining'] < country['positions']:
            continue
        else:
            schools[ind]['countries'].append(countries.pop(0))
            schools[ind]['remaining'] = schools[ind]['remaining'] - country['positions']
            if schools[ind]['remaining'] <= int((1.00-percentageCountry)*schools[ind]['delegates']):
                schoolsOnNextStage.append(schools.pop(ind))
                removeFromPriority(schoolName)
            return
            
    # if the function gets here, it wasn't able to assign the country: move it to the end
    countries.append(country)
    countries.pop(0)
        
def findIndexOfSchool(schoolName):
    for i in range(len(schools)):
        if schools[i]['school'] == schoolName:
            return i
    raise Exception("Can't find " + schoolName + " in the list")
    
def removeFromPriority(schoolName):
    i = 0
    while i < len(school_priority_list):
        if school_priority_list[i] == schoolName:
            school_priority_list.pop(i)
        else:
            i = i + 1


# ### algorithmCountries() loop to assign countries; if there are remaining schools, add them to the schoolsOnNextStage array at the end

# In[9]:


def algorithmCountries():
    maxIterations = 10000
    currIteration = 0
    while not doneCountries(currIteration,maxIterations):
        assignCountry()
        currIteration = currIteration + 1
    for school in schools:
        schoolsOnNextStage.append(school)


# In[10]:


algorithmCountries()
schoolsOnNextStage[0:3]


# In[11]:


countries[0:3]


# In[12]:


finishedSchools = []

def doneCharacters(currIteration,maxIterations):
    if currIteration >= maxIterations:
        return True
    if len(schoolsOnNextStage) == 0:
        return True
    if len(characters) == 0:
        return True
    return False

def assignCharacters():
    if len(schoolsOnNextStage) == 0:
        return
    
    randInt = randint(0, len(schoolsOnNextStage) - 1)
    if schoolsOnNextStage[randInt]['remaining'] == 0:
        return
    else:
        schoolsOnNextStage[randInt]['characters'].append(characters.pop(0))
        schoolsOnNextStage[randInt]['remaining'] = schoolsOnNextStage[randInt]['remaining'] - 1

def removeZeroRemaining():
    i = 0
    while i < len(schoolsOnNextStage):
        if schoolsOnNextStage[i]['remaining'] == 0:
            finishedSchools.append(schoolsOnNextStage.pop(i))
        else:
            i = i + 1
        
def algorithmCharacters():
    maxIterations = 10000
    currIteration = 0
    while not doneCharacters(currIteration,maxIterations):
        removeZeroRemaining()
        assignCharacters()
        currIteration = currIteration + 1
    for school in schoolsOnNextStage:
        finishedSchools.append(school)
        
algorithmCharacters()
finishedSchools[0:3]


# In[13]:


characters[0:3]


# In[14]:


with open('output.csv','w') as fp:
    fp.write("School,Delegates,Remaining\n")
    for school in finishedSchools:
        line = ""
        line += school['school'] + ','
        line += str(school['delegates']) + ','
        line += str(school['remaining']) + ','
        for country in school['countries']:
            line += country['country'] + " (" + str(country['positions']) + "),"

            #make a separate one without the psotiions in it
        for character in school['characters']:
            line += character['character'] + ","
        if line.endswith(','):
            line = line[:-1] + "\n"
        else:
            line = line + "\n"
        fp.write(line)