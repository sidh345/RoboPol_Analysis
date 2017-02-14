from astroquery.vizier import Vizier

#import astroquery.utils.TableList 

import os

from astropy.table import Table
from astropy.coordinates import SkyCoord
import astropy.units as u


def result(c):
    output = Vizier.query_region(c, width = 0.006*u.degree, catalog = ['Gaia DR1 TGAS'])
    return output



os.chdir("/media/siddharth/Seagate Backup Plus Drive/DATA/RoboPol/Catalog/Candidates")

t = Table.read("Q=1.5candidates.dat", format='ascii')
print t

RA = t['RA']
DEC = t['Dec']


for k in range(len(RA)):
    b = SkyCoord(ra = RA[k], dec= DEC[k], unit=(u.deg, u.deg), frame='icrs')
    data = result(b)
    #print data
    length = len(data)
    if length == 1:
        for l in range(length):
            tab = data[l]
            tab.write("/home/siddharth/Desktop" + "/" + str(k) +".dat", format ='ascii')

    if length >= 2:
        tab = data[1]
        tab.write("/home/siddharth/Desktop" + "/" + str(k) +".dat", format ='ascii')
        #print tab

    else:
        print "Object not found"

