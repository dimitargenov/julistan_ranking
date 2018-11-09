from StravaRequest import StravaRequest
import StravaConfig
from GoogleSpreadSheet import GoogleSpreadSheet
import numpy as np
import datetime
import math

now = datetime.datetime.now()

JULBEM_SPREADSHEET_ID = '1UsFnri7Dfcl0ETlHfVSOMrsCIGoCQOnLIQHC__GMwWs'
SAMPLE_RANGE_NAME = 'Class Data!A2:E'
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
    #athlete.append(row['moving_time'])
    #athlete.append(row['elapsed_time'])
    #athlete.append(row['athlete_id'])
    #athlete_picture_url
    #num_activities
    return athlete

def main():
    # strava = StravaRequest(StravaConfig.url, StravaConfig.headers)
    # leaderboard = strava.getLeaderboard()
    # tableHeaderRow = ['Athlete', 'Distance', 'Elevation gain (m)', 'Pace', 'KJ', 'Points']
    # values = []
    # counter = 1
    # for row in leaderboard.json()['data']:
    #     values.append(fillInAthleteInfo(row))
    #     counter += 1

    # sortedResults = sortByPoints(values)
    # sortedResults.insert(0, tableHeaderRow)
    # sortedResults.append(['Last update', now.strftime("%Y-%m-%d %H:%M")])

    ## Read from spreadsheet
    athletes = []
    spreadsheet = GoogleSpreadSheet()
    rangeName = "W1!C3:M"
    w1 = spreadsheet.read(rangeName, JULBEM_SPREADSHEET_ID)
    athletes = addToGeneral(w1)

if __name__ == '__main__':
    main()