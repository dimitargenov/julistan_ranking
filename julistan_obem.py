from StravaRequest import StravaRequest
import StravaConfig
from GoogleSpreadSheet import GoogleSpreadSheet
import numpy as np

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
    return sorted(values, key=lambda a_entry: a_entry[6], reverse = True) 

def main():
    strava = StravaRequest(StravaConfig.url, StravaConfig.headers)
    leaderboard = strava.getLeaderboard()
    tableHeaderRow = ['Rank', 'Athlete', 'Distance', 'Elevation gain (m)', 'Pace', 'KJ', 'Points']
    values = []
    for row in leaderboard.json()['data']:
        paceMin = 0
        paceSec = 0
        [paceMin, paceSec] = calculatePace(row['moving_time'],row['distance'])
        distance = float(row['distance']/1000)
        elevation = int(row['elev_gain'])
        athlete = list()
        athlete.append(row['rank'])
        athlete.append(row['athlete_firstname'] + ' ' + row['athlete_lastname'])
        athlete.append(round(distance,2))
        athlete.append(elevation)
        athlete.append(str(paceMin) + ':' + str(paceSec).zfill(2))
        athlete.append(calculateCoefJulqga(paceMin, paceSec))
        athlete.append(calculatePoints(distance, elevation, calculateCoefJulqga(paceMin, paceSec)))
        #athlete.append(row['moving_time'])
        #athlete.append(row['elapsed_time'])
        #athlete.append(row['athlete_id'])
        #athlete_picture_url
        #num_activities
        values.append(athlete)

    sortedResults = sortByPoints(values)
    sortedResults.insert(0, tableHeaderRow)

    ## Write to spreadsheet
    spreadsheet = GoogleSpreadSheet()
    range_name = "Sheet1!B3:M"
    spreadsheet.write(range_name, sortedResults, JULBEM_SPREADSHEET_ID)

if __name__ == '__main__':
    main()