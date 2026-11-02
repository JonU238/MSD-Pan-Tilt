import math
import numpy as np
import csv

def llh_to_ecef(latitude, longitude, height):
    F = 1/298.257223563
    A = 6378137.0
    A2 = A * A
    B = A * (1 - F)
    B2 = B * B
    E2 = (A2 - B2) / A2
    EP2 = (A2 - B2) / B2
    
    lat = latitude / 180 * math.pi
    lon = longitude / 180 * math.pi

    sin_lat = math.sin(lat)
    cos_lat = math.cos(lat)
    sin_lon = math.sin(lon)
    cos_lon = math.cos(lon)

    roc = A2 / math.sqrt(A2 * cos_lat * cos_lat + B2 * sin_lat * sin_lat)

    x = (roc + height) * cos_lat * cos_lon
    y = (roc + height) * cos_lat * sin_lon
    z = (B2 / A2 * roc + height) * sin_lat

    return [x, y, z]

def LLHtoAE(tlat,tlon,th,rlat,rlon,rh):
    #Elevation code
    tr = np.array(llh_to_ecef(tlat,tlon,th))
    rr = np.array(llh_to_ecef(rlat,rlon,rh))
    dr = tr-rr
    thetaE = math.pi*0.5-math.acos(np.dot(rr,dr)/(np.linalg.norm(rr)*np.linalg.norm(dr)))

    #Azumith code
    

    return(thetaE)