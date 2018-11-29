
class Helper:
    def formatNumber(number, digits):
        return np.format_float_scientific(number, precision=1)

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

    @staticmethod    
    def fillInAthleteInfo(self, row):
        paceMin = 0
        paceSec = 0
        [paceMin, paceSec] = self.calculatePace(row['moving_time'],row['distance'])
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