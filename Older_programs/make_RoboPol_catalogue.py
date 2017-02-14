"""
Task1:

First task is to create a catalog of all objects discovered in the RoboPol fields. I will use the following alogrithm to find an object across all the epochs of the field and store the corresponding data in an astropy table.

The code below, after listing all the data files of the field inside the Output Directory, does the following:

1. Take an object in the first row of the first epoch's csv data o/p file. 
2. Extract it's details(x,y,Ra,Dec,p,sig_p,theta,sig_theta,mag,sig_mag)
3. Scan through all other csv files of other other epochs, find the corresponding object and it's details in that epoch.
4. Repeat this step for all other objects in the first epoch csv file.
5. Write this data in an astropy table for each object. 
6. Create a catlogue of all objects in the field.
7. Store the data in a common directory for all fields as well a seperate directory for each field.
"""


import glob2
from astropy.table import Table
import numpy
import os, shutil


Data_Analysis_Dir = os.path.join("/media/siddharth/Seagate Backup Plus Drive/DATA/RoboPol/","Analysis")
Catalog_Dir = os.path.join("/media/siddharth/Seagate Backup Plus Drive/DATA/RoboPol/","Catalog")
if not os.path.exists(Data_Analysis_Dir):
    os.mkdir(Data_Analysis_Dir)

if not os.path.exists(Catalog_Dir):
    os.mkdir(Catalog_Dir)
 
def Make_Catalog(blazar):
        
    print "Starting analysis of data.csv files for", blazar
    
    #Go to the main result directry for the field.
    Data_Dir = "/media/siddharth/Seagate Backup Plus Drive/DATA/RoboPol/Output_Data/" + blazar
    os.chdir(Data_Dir)
    print "Currently in",os.getcwd()

    # lists all data.csv files in for all epochs of the blazar observations
    data_files = glob2.glob("*/data.csv")               #epoch/data.csv
    for a , b in enumerate(data_files):
        print a , b

    analysis_dir = os.path.join(Data_Analysis_Dir, blazar)
    if not os.path.exists(analysis_dir):                #make a directory to contain all the analysis files for a field
        os.mkdir(analysis_dir)

    #open the first data.csv file
    a = open(data_files[0],'r')
    f = a.readlines()    # collects the data in form of string of strings

    margin = 0.003   #margin to find an object within that error rA  and Dec radius
    #snr = 03.0       #a cut off snr for p measurement. Magnitude is not an issue


    for k in range(3,len(f)):              #actual data content starts from the fourth line onwards
        tab = Table()                      # create an astropy table for each object in the field
        tab = Table(names=('ObjectNo', 'Epoch', 'X-coord', 'Y-coord', 'RA', 'Dec', 'p', 'sig_p', 'theta', 'sig_theta', 'mag', 'sig_mag'))#, dtypes=('i4', 'i4', 'f16','f16','f16','f16','f16','f16','f16','f16', 'f16', 'f16' ))
        b = f[k].split(",")                #b is a list containing all the numbeers for the object k.it is a csv file, so all entries are seperated by a comma. This returns a list of strings(numbers as strings)
        X = float(b[0])
        Y = float(b[1])
        Ra = float(b[2])                  #in degrees
        Dec = float(b[3])                 #in degrees
        p = float(b[4])
        sig_p = float(b[5])
        p_snr = p/sig_p
        theta = float(b[6])               #in radians
        sig_theta = float(b[7])           #in radians
        theta_snr = theta/sig_theta
        mag = float(b[16])
        sig_mag = float(b[17])
        mag_snr = mag/sig_mag
        data1 = k-2, 1, X, Y, Ra, Dec, p, sig_p, theta, sig_theta, mag, sig_mag   #list of data to be written to a table
        #if p_snr >= snr:
        tab.add_row(data1)
        
        for m in range(1,len(data_files)):
            c = open(data_files[m],'r')
            g = c.readlines()
            for s in range(3,len(g)):
                t = g[s].split(",")                   #analogus quantity to b in teh earlier lines
                A = float(t[4])/float(t[5])           #p_snr
                B = float(t[6])/float(t[7])           #theta_snr
                #C = float(t[16])/float(t[17])         #mag_theta
                
                if abs(float(Ra) - float(t[2])) <= margin and abs(float(Dec) - float(t[3])) <= margin:
                    data2 = k-2, m+1, float(t[0]),float(t[1]),float(t[2]),float(t[3]), float(t[4]), float(t[5]) , float(t[6]), float(t[7]),float(t[16]),float(t[17])
                    #if A >= snr:
                    tab.add_row(data2)
        tab.write(analysis_dir +"/" + field + '_'+ str(k-2) + '.dat', format = 'ascii')          #file in which the data for a given star is written
    
    data_files = os.listdir(analysis_dir)
    for item in data_files:
        shutil.copy(analysis_dir+"/"+item, Catalog_Dir)


os.chdir("/media/siddharth/Seagate Backup Plus Drive/DATA/RoboPol/Output_Data/")

RBPL_Fields = os.listdir(os.getcwd())

for a, b in enumerate(RBPL_Fields):
    print a, b

for field in RBPL_Fields:
    Make_Catalog(field)

print "Catalog Created"
##end of code     





