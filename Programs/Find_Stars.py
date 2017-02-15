"""
Task:

Task is to create a table each for all objects discovered in the RoboPol fields. I will use the following alogrithm to find an object across all the epochs of the field and store the corresponding data in an astropy table.

The code below, after listing all the data files of the field, does the following:

1. Take an object in the first row of the first epoch's astropy dat file. 
2. Extract it's details(x,y,Ra,Dec,q,sig_q,u,sig_u,mag,sig_mag)
3. Scan through all other csv files of other other epochs, find the corresponding object and it's details in that epoch.
4. Repeat this step for all other objects in the first epoch dat file.
5. Write this data in an astropy table for each object. 
6. Create a catlogue of all objects in the field.
7. Store the data in a common directory with a seperate directory for each field.

#Right now I am not putting any SNR cuts on P. Will do that later. 

"""

import glob2
from astropy.table import Table
import numpy 
import os, shutil
import math


# Analysis Directory: where all objects for each of the fields will be stored, field wise.

Data_Analysis_Dir = os.path.join("/media/user/Seagate Backup Plus Drive/DATA/RoboPol/","RoboPol_Stars")

if not os.path.exists(Data_Analysis_Dir):
    os.mkdir(Data_Analysis_Dir)

def Make_Catalog(blazar):
        
    print "Starting analysis of data for", blazar
    
    #Go to the main result directry for the field.
    Data_Dir = "/media/user/Seagate Backup Plus Drive/DATA/RoboPol/Corrected_Fields/" + blazar
    os.chdir(Data_Dir)
    print "Currently in",os.getcwd()

    # lists all astropy tables storing data one epoch each of the blazar observations
    data_files = glob2.glob("*.dat")               #epoch/data.csv

    data_files = sorted(data_files, key=os.path.getsize, reverse=True) #to create a list with decreasing size of astropy table, to make the file with largest no of stars in the field the first element of the list, the need of which can be seen from the lines of code below.

    for a , b in enumerate(data_files):
        print a , b

    analysis_dir = os.path.join(Data_Analysis_Dir, blazar)
    if not os.path.exists(analysis_dir):                #make a directory to contain all the analysis files for a field
        os.mkdir(analysis_dir)

    margin = 0.0010   #margin to find an object within that error rA  and Dec radius, equals about 6/7 arc seconds.
    #snr = 2.5       #a cut off snr for p measurement. Magnitude is not an issue
    syserr = 0.0034   #error due to the model emplyed


    #open the first astropy table
    f = Table.read(data_files[0],format ='ascii')  #open the first table

    for k in range(len(f)):              #actual data content starts from the fourth line onwards
        tab = Table()                      # create an astropy table for each object in the field
        tab = Table(names=('ObjectNo', 'Epoch', 'X-coord', 'Y-coord', 'RA', 'Dec','p','error_p','Theta', 'q', 'error_q', 'u', 'error_u', 'mag', 'error_mag','Fair','Year','Month','Date'))#, dtypes=('i4', 'i4', 'f8','f8','f8','f8','f8','f8','f8','f8', 'f8', 'f8','S8','S8','S8' ))
        
        b = f[k]       #b is an astropy row

        dat = data_files[0].split("_")  #get year, month and date
        year = dat[0]
        month = dat[1]
        date = dat[2]
        

        X = float(b[0])
        Y = float(b[1])
        Ra = float(b[2])                  #in degrees
        Dec = float(b[3])                 #in degrees

        p = float(b[4])
        #sig_p = float(b[5])
        #p_snr = p/sig_p

        q = float(b[6])
        sig_Q = float(b[7])
        sig_q = (((sig_Q)**2) + ((syserr)**2))**0.5                 #corrected error due to model
        q_snr = q/sig_q

        u = float(b[8])               
        sig_U = float(b[9]) 
        sig_u = (((sig_U)**2) + ((syserr)**2))**0.5               #corrected error due to model
        u_snr = u/sig_u

        mag = float(b[10])
        sig_mag = float(b[11])
        mag_snr = mag/sig_mag

        Theta = float(b[12])
        theta = Theta*(180/math.pi)                                 #convert theta from radians to degrees 

        fair = b[13]                                                #whether object is fair

        sig_p = ((((sig_q**2)*(q**2)) + ((sig_u**2)*(u**2)))/((q**2) + (u**2)))**0.5

        p = (abs((p**2)-(sig_p**2)))**(0.5)  #debiasing p measurement.
        p_snr = p/sig_p

        data1 = k, 0, X, Y, Ra, Dec, p, sig_p,theta, q, sig_q, u, sig_u, mag, sig_mag, fair year, month, date   #list of data to be written to a table

        
        #if p_snr >= snr:# and q_snr >= snr:
        tab.add_row(data1)
        
        for m in range(1,len(data_files)):
            g = Table.read(data_files[m], format='ascii')
            for s in range(len(g)):
                t = g[s]                   #analogus quantity to b in the earlier lines
                P = float(t[4])           #p value
                Q = t[6]
                U = t[8]
                q_error =  (((t[7])**2) + ((syserr)**2))**0.5   #corrected error in q
                u_error =  (((t[9])**2) + ((syserr)**2))**0.5   #corrected error in u
                Q_snr = t[6]/q_error   #snr of q
                U_snr = t[8]/u_error   #snr of u

                sig_P = ((((q_error**2)*(Q**2)) + ((u_error**2)*(U**2)))/((Q**2) + (U**2)))**0.5

                P_snr = P/sig_P

                FAIR = t[13]                # is the object fair?

                DATE = data_files[m].split("_")
                Year = DATE[0]
                Month = DATE[1]
                Date = DATE[2]
                #DATE = str(("[0_").join(DATE))


                #if P_snr >= snr:# and U_snr >= snr:
                if abs(Ra - float(t[2])) <= margin and abs(Dec - float(t[3])) <= margin:

                    data2 = k, m, float(t[0]),float(t[1]),float(t[2]),float(t[3]), float(t[4]), sig_P, (180/math.pi)*float(t[12]), Q, q_error, U, u_error,float(t[10]),float(t[11]),FAIR, Year, Month, Date
                    tab.add_row(data2)

        tab.write(analysis_dir +"/" + blazar + '_'+ str(k) + '.dat', format = 'ascii')          #file in which data from all epochs of a given star is written
        print "A new star found", str(blazar)+"_"+str(k)
        
    print "All stars found for the field: ", blazar
    


corrected_fields = os.listdir("/media/user/Seagate Backup Plus Drive/DATA/RoboPol/Corrected_Fields/")  #list of fields corrected

star_fields = os.listdir("/media/user/Seagate Backup Plus Drive/DATA/RoboPol/RoboPol_Stars/") #fields for whiich Stars have been found

blazar_list = [x for x in corrected_fields if x not in star_fields]   #new fields for which stars have to be found.


for z in blazar_list:
    print z
    Make_Catalog(z)

print "Stars Found"

 
#revised and verified this code on 3 Feb, 2017.
#revision 2: added snr cut off based on revised p from syserror. Feb 6, 2017.
#revision 3: verified on 8 Feb, 2017.
#revision attempt 3: trying to include date info in star table. 8 Feb, 8.52 pm starting. Done successfully.
#revision 4: trying to add bollean character to the stars table.

##end of code     





