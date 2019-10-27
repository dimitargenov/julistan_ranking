from StravaRequest import StravaRequest
import StravaConfig
from GoogleSpreadSheet import GoogleSpreadSheet
import numpy as np
import datetime
import math

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
    return sorted(values, key=lambda a_entry: a_entry[5], reverse = True) 

def displayNumber(value):
    return 1

def fillInAthleteInfo(row):
    paceMin = 0
    paceSec = 0
    [paceMin, paceSec] = calculatePace(row['moving_time'],row['distance'])
    distance = float(round(row['distance']/1000,1))
    elevation = int(math.ceil(row['elev_gain']))
    name = row['athlete_firstname'] + ' ' + row['athlete_lastname']
    pace = str(paceMin) + ':' + str(paceSec).zfill(2)
    kj = calculateCoefJulqga(paceMin, paceSec)
    points = calculatePoints(distance, elevation, calculateCoefJulqga(paceMin, paceSec))

    athlete = list()
    athlete.append(name)
    athlete.append(str(distance).zfill(1))
    athlete.append(elevation)
    athlete.append(pace)
    athlete.append(kj)
    athlete.append(points)

    return athlete

def addRank(athletes):
    counter = 0
    for row in athletes:
        counter += 1
        row.insert(0, counter)

def addDiff(athletes):
    leaderPoints = 0
    counter = 0
    for row in athletes:
        if leaderPoints == 0:
            leaderPoints = row[6]
            continue
        diff = float(leaderPoints) - float(row[6])
        row.append(diff)

def main():
    strava = StravaRequest(StravaConfig.url, StravaConfig.headers)
    leaderboard = strava.getLeaderboard()
    tableHeaderRow = ['Pos','Athlete', 'Distance[km]', 'D+[m]', 'Pace[min/km]', 'KJ', 'Total', 'Diff']

    values = []
    counter = 1
    previousPoints = 0
    for row in leaderboard.json()['data']:
        values.append(fillInAthleteInfo(row))

    sortedResults = sortByPoints(values)
    addRank(sortedResults)
    addDiff(sortedResults)
    sortedResults.insert(0, tableHeaderRow)
    sortedResults.append(['','Last update', now.strftime("%Y-%m-%d %H:%M")])

    ## Write to spreadsheet
    spreadsheet = GoogleSpreadSheet()
    rangeName = "W1!B3:M"
    spreadsheet.write(rangeName, sortedResults, JULBEM_SPREADSHEET_ID)

if __name__ == '__main__':
    main()