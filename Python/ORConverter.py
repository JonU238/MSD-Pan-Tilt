import math
import numpy as np
import csv

F = 1/298.257223563
A = 6378137.0
A2 = A * A
B = A * (1 - F)
B2 = B * B
E2 = (A2 - B2) / A2
EP2 = (A2 - B2) / B2

def llh_to_ecef(latitude, longitude, height):
    '''Convert (latitude, longitude, height) in LLH to (x, y, z) in ECEF.
    '''

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

# ordata should be Time, Alt, Vertical Vel, Lateral direction, Lateral Vel, Lat[deg],Lon[deg]
ordata = np.loadtxt("SampleRocket.csv", delimiter=",")
print(ordata[:,0])
time = ordata[:,0]
alt = ordata[:,1]
vv = ordata[:,2]
heading = ordata[:,3]
lateralvel = ordata[:,4]
rlat = ordata[:,5]
rlon = ordata[:,6]

ecefpos = []
for i in range(np.size(time)):
    ecefpos.append(llh_to_ecef(rlat[i].item(),rlon[i].item(),alt[i].item()))

print(ecefpos)
