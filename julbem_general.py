from StravaRequest import StravaRequest
import StravaConfig
from GoogleSpreadSheet import GoogleSpreadSheet
import numpy as np
import datetime
import math

now = datetime.datetime.now()

JULBEM_SPREADSHEET_ID = '1UsFnri7Dfcl0ETlHfVSOMrsCIGoCQOnLIQHC__GMwWs'
TICHANE_COEF = 6

def sortByPoints(values):
    return sorted(values, key=lambda a_entry: a_entry[1], reverse = True) 

def displayNumber(value):
    return 1

def addDiff(athletes):
    leaderPoints = 0
    counter = 0
    for row in athletes:
        if leaderPoints == 0:
            leaderPoints = row[1]
            continue
        # print(leaderPoints)
        # exit()
        diff = float(leaderPoints) - float(row[1])
        row.append(diff)

def addToGeneral(weekRanking, athletes):
    for row in weekRanking:
        if (len(row) < 3) or (row[2] == "D+[m]"):
            continue
        if row[0] not in athletes:
            athletes[row[0]] = list()
            athletes[row[0]].append(0)
            athletes[row[0]].append(1) #Total points
            athletes[row[0]].append(0) #Distance
            athletes[row[0]].append(0) #Elevation
        athletes[row[0]][0] = row[0] #Name
        athletes[row[0]][1] += float(row[5]) #Total points
        athletes[row[0]][2] += float(row[1]) #Distance
        athletes[row[0]][3] += int(row[2]) #Elevation

    return athletes

def main():
    ## Read from spreadsheet
    athletes = {}
    spreadsheet = GoogleSpreadSheet()
    weekSheets = ['W1', 'W2', 'W3', 'W4']

    for sheet in weekSheets:
        rangeName = sheet + "!C3:M"
        wRanking = spreadsheet.read(rangeName, JULBEM_SPREADSHEET_ID)
        athletes = addToGeneral(wRanking, athletes)

    tableHeaderRow = ['Athlete', 'Total', 'Distance[km]', 'Elevation[m]', 'Diff']

    sortedResults = sortByPoints(athletes.values())
    addDiff(sortedResults)
    sortedResults.insert(0, tableHeaderRow)
    sortedResults.append(['Last update', now.strftime("%Y-%m-%d %H:%M")])

    ## Write to spreadsheet
    rangeName = "General!C2:M"
    spreadsheet.write(rangeName, sortedResults, JULBEM_SPREADSHEET_ID)   

if __name__ == '__main__':
    main()