#IMPORTS

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.axes as ax


enteredSex = "Male"
enteredNameExists = True

#STARTING INPUTS. User enters start/end years. Can also enter an optional name and sex to search for. Inputs are checked before advancing. 

startYear = input("Enter a starting year between 1880 and 2018.")

while ((startYear.isdigit() == False) or ((int(startYear) > 2018) or (int(startYear) < 1880))):
    startYear = input("Error. Enter a starting year between 1880 and 2018.")
startYear = int(startYear)
while ((startYear > 2018) or (startYear < 1880)):
    startYear = input("Error. Enter a starting year between 1880 and 2018.")

maxYear = input("Enter an ending year between 1880 and 2018. Must be the same or after starting year.")


while (maxYear.isdigit() == False):
    maxYear = input("Error. Enter an ending year between 1880 and 2018. Must be the same or after starting year.")
maxYear = int(maxYear)
while ((maxYear > 2018) or (maxYear < 1880) or (startYear > maxYear)):
    maxYear = input("Error. Enter an ending year between 1880 and 2018. Must be the same or after starting year.")

enteredName = input("Optional: Enter the name you are searching for data on. To skip, enter NONE.")

if (enteredName == "NONE"):
    enteredNameExists = False

if (enteredNameExists == True):
    enteredSex = input("Enter the gender of the name you are searching for.")
    while ((enteredSex != "Male") and (enteredSex != "Female")):
        enteredSex = input("Error. Enter the gender of the name you are searching for.")


countByYear__Male = []
countByYear__Female = []
percentageByYear = []
currentYear = startYear

#LOOP THROUGH ALL FILES WITHIN SPECIFIED YEAR RANGE

while(currentYear < (maxYear + 1)):

   

    currentList = []
    maleNames = []
    femaleNames = []
    maleCount = []
    femaleCount = []


    currentFileName = "yob{}.txt".format(currentYear) #Open file based on currentYear varible.

    

    File_object = open(currentFileName,"r")
    currentList = File_object.readlines()
    File_object.close() # Always be sure to close any opened files.

    i = 0

    for dataSet in currentList:

        #Extract variables from each line of the current file based on comma location. 
        currentDataSet = currentList[i]
        i = i + 1
        commaLocation = currentDataSet.index(",")

        currentName = currentDataSet[0:commaLocation]
        currentSex = currentDataSet[(commaLocation + 1):(commaLocation + 2)]
        currentCount = currentDataSet[(commaLocation + 3):]
        currentCount = int(currentCount)


        #Split data based on sex

        if (currentSex == "F"):

            #Female List

            femaleNames.append(currentName)
            femaleCount.append(currentCount)



        else:

            #Male List

            maleNames.append(currentName)
            maleCount.append(currentCount)

    #For every year being processed, create a DataFrame for each sex.

    maleDataFrame = pd.DataFrame({"Year":currentYear,"Name":maleNames,"Count":maleCount})
    femaleDataFrame = pd.DataFrame({"Year":currentYear,"Name":femaleNames,"Count":femaleCount})

    countByYear__Male.append(maleDataFrame['Count'].sum(axis = 0, skipna = True))
    countByYear__Female.append(femaleDataFrame['Count'].sum(axis = 0, skipna = True))


    #Combine these DataFrames into two "Master" DataFrames, one male, one female.

    if (currentYear == startYear):

        masterMaleDataFrame = maleDataFrame
        masterFemaleDataFrame = femaleDataFrame

    if (currentYear >startYear):

        masterMaleDataFrame = pd.concat([masterMaleDataFrame,maleDataFrame], ignore_index=True)
        masterFemaleDataFrame = pd.concat([masterFemaleDataFrame,femaleDataFrame],ignore_index=True)

    currentYear = currentYear + 1


#Create dictionaries that go through the Master DataFrames and combine the counts of each name.

masterMaleDictionary = {}
masterFemaleDictionary = {}

for index, row in masterMaleDataFrame.iterrows():


    currentRowName = row['Name']
    currentRowCount = row['Count']

    if currentRowName not in masterMaleDictionary:
        #Add new entry to dictionary

        masterMaleDictionary.update({currentRowName:currentRowCount})

    else:
        oldTotal = masterMaleDictionary.get(currentRowName)
        newTotal = oldTotal + currentRowCount

        masterMaleDictionary.update({currentRowName:newTotal})

        #Update dictionary key value via addition


for index, row in masterFemaleDataFrame.iterrows():


    currentRowName = row['Name']
    currentRowCount = row['Count']

    if currentRowName not in masterFemaleDictionary:
        #Add new entry to dictionary

        masterFemaleDictionary.update({currentRowName:currentRowCount})

    else:
        oldTotal = masterFemaleDictionary.get(currentRowName)
        newTotal = oldTotal + currentRowCount

        masterFemaleDictionary.update({currentRowName:newTotal})

        #Update dictionary key value via addition

#Create DataFrames from dictionaries that reflect the results across all included years. 

totalMaleDataFrame = pd.DataFrame(masterMaleDictionary.items(),columns = ['Name','Count'])
totalMaleDataFrame = totalMaleDataFrame.sort_values('Count', ascending = False)
totalMaleDataFrame = totalMaleDataFrame.reset_index(drop=True)

totalFemaleDataFrame = pd.DataFrame(masterFemaleDictionary.items(),columns = ['Name','Count'])
totalFemaleDataFrame = totalFemaleDataFrame.sort_values('Count', ascending = False)
totalFemaleDataFrame = totalFemaleDataFrame.reset_index(drop=True)

maleTop10 = totalMaleDataFrame.head(10)
femaleTop10 = totalFemaleDataFrame.head(10)
maleTotalCount = totalMaleDataFrame['Count'].sum(axis = 0, skipna = True)
femaleTotalCount = totalFemaleDataFrame['Count'].sum(axis = 0, skipna = True)

#Calculate percentage of each top name. 

femalePercentageList = []
femaleNameList__ForPieChart = []
malePercentageList = []
maleNameList__ForPieChart = []

for index, row in maleTop10.iterrows():
    currentNameCount = row['Count']
    currentPercentage = currentNameCount / maleTotalCount
    currentPercentage = currentPercentage * 100
    currentPercentage = round(currentPercentage, 2)
    malePercentageList.append(currentPercentage)
    maleNameList__ForPieChart.append(row['Name'])

for index, row in femaleTop10.iterrows():
    currentNameCount = row['Count']
    currentPercentage = currentNameCount / femaleTotalCount
    currentPercentage = currentPercentage * 100
    currentPercentage = round(currentPercentage, 2)
    femalePercentageList.append(currentPercentage)
    femaleNameList__ForPieChart.append(row['Name'])


#Create Pie/Donut charts showing the percentage of babies born with the top names.

# SET UP MALE PIE CHART

otherVal = 100

for val in malePercentageList:
    otherVal = otherVal - val

malePercentageList__ForPieChart = malePercentageList
malePercentageList__ForPieChart.append(otherVal)
maleNameList__ForPieChart.append("Other")

# SET UP FEMALE PIE CHART

otherVal = 100

for val in femalePercentageList:
    otherVal = otherVal - val

femalePercentageList__ForPieChart = femalePercentageList
femalePercentageList__ForPieChart.append(otherVal)
femaleNameList__ForPieChart.append("Other")

plt.figure(0)
plt.subplot(121)

plt.pie(malePercentageList__ForPieChart, labels= maleNameList__ForPieChart, pctdistance=0.85, autopct='%1.1f%%', startangle=220, rotatelabels=True, wedgeprops={"edgecolor":"0",'linewidth': 1,})
plt.title("Top Male Baby Names From {} — {}".format(startYear,maxYear),y=1.08)
centre_circle = plt.Circle((0,0),0.75,color='black', fc='white',linewidth=1.25)
fig = plt.gcf()
fig.gca().add_artist(centre_circle)

plt.axis('equal')



#plt.figure(1)
plt.subplot(122)

plt.pie(femalePercentageList__ForPieChart, labels= femaleNameList__ForPieChart, pctdistance=0.85, autopct='%1.1f%%', startangle=270, rotatelabels=True, wedgeprops={"edgecolor":"0",'linewidth': 1,})
plt.title("Top Female Baby Names From {} — {}".format(startYear,maxYear),y=1.08)
centre_circle = plt.Circle((0,0),0.75,color='black', fc='white',linewidth=1.25)
fig = plt.gcf()
fig.gca().add_artist(centre_circle)

plt.axis('equal')

#If the user entered a name, calculate the percentage of babies with that name during the specified timeframe.

plt.figure(1)

if (enteredSex == "Male"):

    enteredNameCount__Male = masterMaleDictionary.get(enteredName)

    if (enteredNameCount__Male is None):

        print("No records of entered name were found.")
        enteredNameExists = False
    else:

        enteredNamePercentage = enteredNameCount__Male / maleTotalCount
        enteredNamePercentage = enteredNamePercentage * 100
        otherVal = 100 - enteredNamePercentage

        #plt.figure(2)
       
        plt.subplot(221)
        plt.pie([enteredNamePercentage,otherVal], explode=(0.1,0), labels= [enteredName,"Other"], autopct='%1.3f%%', startangle=90,wedgeprops={"edgecolor":"0",'linewidth': 1,})
        plt.title("Percentage of Male Babies Named {} From {} — {}".format(enteredName,startYear,maxYear))

if (enteredSex == "Female"):

    enteredNameCount__Female = masterFemaleDictionary.get(enteredName)

    if (enteredNameCount__Female is None):

        print("No records of entered name were found.")
        enteredNameExists = False
    else:


        enteredNamePercentage = enteredNameCount__Female / femaleTotalCount
        enteredNamePercentage = enteredNamePercentage * 100
        otherVal = 100 - enteredNamePercentage

        #plt.figure(2)
        plt.subplot(221)
        plt.pie([enteredNamePercentage,otherVal], explode=(0.1,0), labels= [enteredName,"Other"], autopct='%1.3f%%', startangle=90,wedgeprops={"edgecolor":"0",'linewidth': 1,})
        plt.title("Percentage of Female Babies Named {} From {} — {}".format(enteredName,startYear,maxYear))


#COUNT OF SPECIFIED NAME BY YEAR

nameByYear__Years = []
nameByYear__Counts = []
yearList = []

for index, row in masterMaleDataFrame.iterrows():
    if (row['Year'] not in yearList):
        yearList.append(row['Year'])


if (enteredNameExists == True):

    #Female

    if (enteredSex == "Female"):
        for index, row in masterFemaleDataFrame.iterrows(): 
            
            if (row['Name'] == enteredName):

                nameByYear__Years.append(row['Year'])
                nameByYear__Counts.append(row['Count'])

    if (enteredSex == "Male"):
        for index, row in masterMaleDataFrame.iterrows(): 

            if (row['Name'] == enteredName):

                nameByYear__Years.append(row['Year'])
                nameByYear__Counts.append(row['Count'])


    #plt.figure(3)
    plt.subplot(222)
    plt.plot(nameByYear__Years,nameByYear__Counts)

    plt.title("Number of Babies Named {} From {} — {}".format(enteredName,startYear,maxYear))
    plt.xlabel("Year")
    plt.ylabel("Number of Babies")


#Count number of babies born per year.

#plt.figure(4)
plt.subplot(223)
plt.plot(yearList,countByYear__Male, color ='red', label='Male')
plt.plot(yearList,countByYear__Female, color = 'blue', label='Female')
plt.title("Number of Babies Born Per Year From {} — {}".format(startYear,maxYear))
plt.xlabel("Year")
plt.ylabel("Number of Babies")
plt.legend()


#plt.figure(5)



if (enteredNameExists == True): #True

    for i in range(len(nameByYear__Counts)):

        if (enteredSex == "Female"):
            currPerc = (nameByYear__Counts[i] / countByYear__Female[i])
            currPerc = currPerc * 100

        else:
            currPerc = (nameByYear__Counts[i] / countByYear__Male[i])
            currPerc = currPerc * 100            


        percentageByYear.append(currPerc)

    #plt.figure(5)
    plt.subplot(224)
    plt.plot(nameByYear__Years,percentageByYear)
    plt.title("Percentage of Babies Named {} From {} — {}".format(enteredName,startYear,maxYear))
    plt.xlabel("Year")
    plt.ylabel("Percentage of Babies")


plt.show()  #Always at end
