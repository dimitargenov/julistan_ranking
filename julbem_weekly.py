# -*- coding: utf-8 -*-

from StravaRequest import StravaRequest
import StravaConfig
from GoogleSpreadSheet import GoogleSpreadSheet
import numpy as np
import datetime
import math
from time import strftime
from time import gmtime

now = datetime.datetime.now()

#2018 sheet
#JULBEM_SPREADSHEET_ID = '1UsFnri7Dfcl0ETlHfVSOMrsCIGoCQOnLIQHC__GMwWs'

#2019
JULBEM_SPREADSHEET_ID = '1TwkR8Z3_lVHx1FF3XcGoK_huhIBeJVmHWroH-DUHnjo'
TICHANE_COEF = 6

def calculatePace(time, distance):
    pace = (float(time)/60)/(float(distance)/1000)
    return (int(pace), int((pace - int(pace))*60))

def calculateCoefJulqga(paceMin, paceSec):
    return round(TICHANE_COEF/(paceMin+1.0*paceSec/60), 2)

def calculatePoints(distance, elevation, kj):
    return round((distance + elevation*0.01)*kj, 1)

def sortByPoints(values):
    return sorted(values, key=lambda a_entry: a_entry[6], reverse = True) 

def displayNumber(value):
    return 1

def fillInAthleteInfo(row):
    paceMin = 0
    paceSec = 0
    [paceMin, paceSec] = calculatePace(row['moving_time'],row['distance'])
    distance = float(round(row['distance']/1000,1))
    elevation = int(math.ceil(row['elev_gain']))
    name = row['athlete_firstname'] + ' ' + row['athlete_lastname'] + addPreviousRank(row)
    pace = str(paceMin) + ':' + str(paceSec).zfill(2)
    kj = calculateCoefJulqga(paceMin, paceSec)
    points = calculatePoints(distance, elevation, calculateCoefJulqga(paceMin, paceSec))
    time = strftime("%H:%M:%S", gmtime(row['moving_time']))
    prediction = strftime("%H:%M:%S", gmtime(getMarathonPrediction(row)))

    athlete = list()
    athlete.append(name)
    athlete.append(str(distance).zfill(1))
    athlete.append(elevation)
    athlete.append(pace)
    athlete.append(kj)
    athlete.append(time)
    #athlete.append(prediction)
    athlete.append(points)

    return athlete

def addRank(athletes):
    counter = 0
    for row in athletes:
        counter += 1
        row.insert(0, counter)

def addPreviousRank(row):
    rankingDict = {u'Ники Дерменджиев': 1, u'Triatlet Maffetonssen': 2, u'Nikolay Nachev': 3, u'Валентин Шишков': 4, u'Metodi Georgiev': 5, 
    u'Radoslav Dachev': 6, u'Lyudmil Nikodimov': 7, u'Alexander Spasov': 8, u'Stella Dimitrova': 9, u'Daniel Kubashliev': 10}
    key = row['athlete_firstname'] + ' ' + row['athlete_lastname']
    if key in rankingDict:
        return ' (' + str(rankingDict[key]) + ')'
    else:
        return ''

def getMarathonPrediction(row):
    [paceMin, paceSec] = calculatePace(row['moving_time'],row['distance'])
    pace = paceMin + float(round(paceSec/60, 1))
    distance = float(round(row['distance']/1000,1))

    return (12+98.5*math.exp(-distance/189)+1390/(60/pace))/1440

def addDiff(athletes):
    leaderPoints = 0
    counter = 0
    for row in athletes:
        if leaderPoints == 0:
            leaderPoints = row[7]
            continue
        diff = float(leaderPoints) - float(row[7])
        row.append(diff)

def main():
    strava = StravaRequest(StravaConfig.url, StravaConfig.headers)
    leaderboard = strava.getLeaderboard()
    tableHeaderRow = ['Pos','Athlete', 'Distance[km]', 'D+[m]', 'Pace[min/km]', 'KJ', 
    'Time', 'Total', 'Diff']

    values = []
    counter = 1
    previousPoints = 0
    for row in leaderboard.json()['data']:
        values.append(fillInAthleteInfo(row))

    sortedResults = sortByPoints(values)
    addRank(sortedResults)
    addDiff(sortedResults)
    #print(sortedResults)
    #exit()
    sortedResults.insert(0, tableHeaderRow)
    sortedResults.append(['','Last update', now.strftime("%Y-%m-%d %H:%M")])

    ## Write to spreadsheet
    spreadsheet = GoogleSpreadSheet()
    rangeName = "W1!B3:M"
    spreadsheet.write(rangeName, sortedResults, JULBEM_SPREADSHEET_ID)

if __name__ == '__main__':
    main()