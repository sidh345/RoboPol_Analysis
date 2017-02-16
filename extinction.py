#These are peices of code written by Gina to create a p Vrs E-V plot for the candidates.

from urllib import urlretrieve
import time
import glob
import os
from matplotlib import rc, font_manager
import numpy as np
from astropy.coordinates import SkyCoord
from astropy import units as u
import matplotlib.pyplot as plt

def parse():
   count = 0
   found_ext = 0
   fop = open('html.html')
   if True:
       for line in fop.readlines():
          if count:
            err = float(line.split()[6])
            break
          if line.startswith("<tr> <td> E(B-V)"):
             Ebv = float(line.split()[5])
             count = 1
             found_ext = 1
   fop.close()
   # if no extinction available for this source
   if not found_ext:
      return np.nan, np.nan
   
   return Ebv, err

def get_extinctions(l,b):
    """Provide lists of l, b in degrees (decimal). Outputs list of extinctions
    """
    prefix = "http://faun.rc.fas.harvard.edu/eschlafly/2dmap/querymap.php?lcoord="
    suffix = "bcoord="

    extinctions = []
    print 'source, l, b, E(B-V), sigma_E(B-V), A_V'
    # Loop over your sources
    for i in range(len(l)):
       li=str(l[i])
       bi=str(b[i])
       url = prefix + li + "&"+ suffix+bi
       # Query the server/map
       urlretrieve(url, 'html.html')
       # Get the E(B-V) value for this source
       Ebv, err = parse()
       # Convert E(B-V) to Av assuming an Rv of 3.1
       extinctions.append(float(Ebv*3.1))
       print i, l[i], b[i], Ebv, err, Ebv*3.1
       time.sleep(1)
    return np.array(extinctions)

READ = False

if READ:
    # Loop over stars and get coordinates and p
    fop = open('/media/user/Seagate Backup Plus Drive/DATA/RoboPol/Candidates/candidates.dat')
    fop.readline()
    ras = []
    decs = []
    ps = []
    stars = []
    for line in fop.readlines():
        sl = line.split()
        ra = float(sl[1])
        ras.append(ra)
        dec = float(sl[2])
        decs.append(dec)
        ps.append(float(sl[3]))

        stars.append(SkyCoord("icrs", ra=ra*u.degree, dec=dec*u.degree))

    # Loop over stars and get their extinction from Schlafly 2014 map
    ext = []
    for i in range(len(stars)):
        l = stars[i].galactic.l.degree
        b = stars[i].galactic.b.degree
        ext.append(get_extinctions([l],[b])[0])

    ext = np.array(ext)
    ps = np.array(ps)


    np.save('Av_schlafly2014.npy',ext)
    np.save('ps.npy', ps)

else:
    ps = np.load('ps.npy')
    ext = np.load('Av_schlafly2014.npy')
# debias p: assume sigma_p = p/3
p_d = np.sqrt(ps**2-(ps/3.)**2)

plt.scatter(ext,p_d, marker='+')
Av = np.linspace(0.0001,1.4, 50)
plt.plot(Av,0.0305*Av, c = 'r')
plt.axhline(0.04, c = 'k',ls = '--')
plt.ylim(ymin = 0, ymax = 0.11)
plt.xlim(xmin = 0)
plt.xlabel('$A_V$')
plt.ylabel('p_debiased')
plt.savefig('/media/user/Seagate Backup Plus Drive/DATA/RoboPol/Candidates/p-Av-schlafly14.png')
plt.show()

