import os, shutil 
import numpy as np
from pipeline import robopol_pipeline
import math
import subprocess
import sys
import glob2  #has recursive atribute that simple glob does not have
import pyfits

"""
part A: Steps:
1. Take the name of the RBPL field as input.
2. Find all the science images of an object.
3. Copy them to a seperate directory for each night, inside a directory for the field.
"""

# Name of the target field
blazar = 'RBPLJ0017+8135' 
print blazar
#main data directory, will have to edited when used on a different m/c.
os.chdir( "/media/siddharth/Seagate Backup Plus Drive/DATA/RoboPol/") 


#Create a directory where all the images of the blazar are going to be temporarily stored

Blzr_DIR = os.path.join(os.getcwd(), blazar) 
if not os.path.exists(Blzr_DIR):
    os.mkdir(Blzr_DIR)
print os.path.basename(Blzr_DIR), "created"

#go to the directory where all the raw data of RoboPOl is stored
os.chdir("/media/siddharth/Seagate Backup Plus Drive/DATA/RoboPol/Raw_Data/data/")


#***********************
#PART A
print "Start of collecting and storing science images of", blazar
#The following commands search for images of the field in the hard disk database, makes a list,
#and copies to a folder in the hard disk titled with the field name/night

images = glob2.glob("*/*/*" + blazar + "*R*.fits")      # "year/night/something" + blazar + "something"
for a,b in enumerate(images):                           #prints all the science images
    print a , b

#lines to find out epochs
epochs = []      #list that will contain all the epochs in which the object was observed     

for k in range(len(images)):
    epoch = images[k].split('/')[-2]  + '_' +  images[k].split('/')[-1].split('_')[0]   #night plus observation ID
    epochs.append(epoch)
    data_dir = os.path.join(Blzr_DIR,epoch)  #directory where the image will be stored, based on the night.
    if not os.path.exists(data_dir):
        os.mkdir(data_dir)
    shutil.copy(images[k],data_dir)

epochs = list(set(epochs))         #a set has only unique entries, so each epoch will only be represented once.
for x ,y in enumerate(epochs):
    print x ,y 


print "images stored in directries within", Blzr_DIR


#**********************************************
# PART B: Analysis of the image files to get polarization
#1. Go the directory where the blazar data from part A is stored.
#2. Make a list of all the directories within it: list of directories named on the epochs.
#3. Enter the epoch folder, make a list of teh fits files, and feed to the pipeline.
#4. Repeat step 3 for all teh epochs of the Blazar.
#**********************************************

print "Start of Polarization analysis of fields of the", blazar

#Go to the directory where all the data of blazar is stored from Part A.
os.chdir(Blzr_DIR) 
print "Now in the", os.getcwd() ,"directory" 

DATA_DIR = os.listdir(Blzr_DIR)               #List of the epochs(directories)

for a, b in enumerate(DATA_DIR):              #prints the list of epochs for the object
    print a ,b


#Create a Directory where the o/p data will be stored for all the epochs:
if not os.path.exists("/media/siddharth/Seagate Backup Plus Drive/DATA/RoboPol/Output_Data/" + blazar):       
    os.mkdir("/media/siddharth/Seagate Backup Plus Drive/DATA/RoboPol/Output_Data/" + blazar)


#now from the list of epochs in DATA_DIR, enter each epoch_dir, make a list of fits files, and feed it to the pipeline.
for l in range(len(DATA_DIR)):
        os.chdir(DATA_DIR[l])                       #enter the epoch-directory
        fits_files = glob2.glob("*.fits")           # gives the content of the directory in a list
	for e ,files in enumerate(fits_files):      #gives list of all the fits files for the night
	    print e, files

        flats_location = '/media/siddharth/Seagate Backup Plus Drive/DATA/RoboPol/Raw_Data/catalogs/flats/'       #location where all the fits files of RoboPol are located. Note that flat fields are available from 23/6/13 onwards.
	output_dir = "/tmp/"+ blazar 
        output_dir = output_dir +"/" + DATA_DIR[l]

        RESULT_DIR = "/media/siddharth/Seagate Backup Plus Drive/DATA/RoboPol/Output_Data/" + blazar # + #"/" + DATA_DIR[l]
        if not os.path.exists(RESULT_DIR):
            os.mkdir("RESULT_DIR")


	bll = robopol_pipeline.robopol_image(name = blazar, stack_lib = 'alipy', photom_method = 4, band = "R", fits_location =fits_files, output_dir = output_dir, flat_dir=flats_location, model_date = '2014_04_30',bias =562, remove_cr_flag=True, reduce_field = True)
     
        # Calculate polarization results
	bll.reduce_polarization()
	print "Polarization analysis of the epoch is over"
	 
        shutil.move(output_dir, RESULT_DIR)
        print "Data moved to the appropriate folder in Hard Disk, epoch no", l,"over."
        
        os.chdir(Blzr_DIR)          #Go back to start position so that loop cn function properly.

print "Polarization Analysis of the field", blazar,"Done"

#********************************
#PART C:

#Part 1:

#The code below, after listing all the data files of the field inside the Output Blazar Directory, does the following:

#1. Take an object in the first row of the first epoch's csv data o/p file. 
#2. Extract it's details(x,y,Ra,Dec,p,sig_p,theta,sig_theta,mag,sig_mag)
#3. Scan through all other csv files of other other epochs, find the corresponding object and it's details in that epoch.
#4. Repeat this step for all other objects in the first epoch csv file.
#5. Write this data in an astropy table for each object. 
#5. Create a catlogue of all objects in the field.

#Part 2:

#In the second part of the code, I sort out possible good candidates. In this stage, the sorting will be liberal.

#1. Create a list of all the tables(objects) created from part C1 of the code.
#2. Analyze each object table, and find the the suitble candidate by using the following filters.
#   a. Should have been observed for atlest 5 epochs.
#   b. The ratio of width of p measurements and median of sig_p should be near to 1. I have put in the code the requirement that the ratio should be between 0.9 
#   to 1.2. Same criterion for Magnitude. 

#Assumptions:
#    1. Any good/bright source will be detectable in all the epochs, so considered sources that are detected in the first epoch only. The assumption is that objects that are fit for our study(bright) will be visible in the epochs.
#        But will have to keep this thing in mind.
        
#    2. I have taken an SNR of 3 as a cut off, based on inputs from Ram. 

#    3. How to find a candidate that is not variable in any of the three parameters- polarization, EVPA, and magnitude. The criteria that I am using now is: find median and standard deviation of polarization of a star(call it the polarization "width"), and find the "median" of polarization error. If median of polarization error about equal to width of polarization, it can be a possible good source to do further analysis.
       
#**********************************

print "Starting analysis of data files"

import glob2
from astropy.table import Table
import numpy
import os, shutil


#Go to the main result directry for the field.
os.chdir("/media/siddharth/Seagate Backup Plus Drive/DATA/RoboPol/Output_Data/" + blazar)
print os.getcwd()

# lists all data.csv files in for all epochs of the blazar observations
data_files = glob2.glob("*/data.csv")               #epoch/data.csv
for a , b in enumerate(data_files):
    print a , b

analysis_dir = "/media/siddharth/Seagate Backup Plus Drive/DATA/RoboPol/Output_Data/" + blazar +"/Analysis"
if not os.path.exists(analysis_dir):                #make a directory to contain all the analysis files for a field
    os.mkdir(analysis_dir)


#open the first data.csv file
a = open(data_files[0],'r')
f = a.readlines()    # collects the data in form of string of strings

# following lines extract the field name
field = blazar
print "Field is", field

margin = 0.003   #margin to find an object within that error rA  and Dec radius
snr = 03.0       #a cut off snr for p measurement. Magnitude is not an issue


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
    if p_snr >= snr:
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
                if A >= snr:
                    tab.add_row(data2)
    tab.write(analysis_dir +"/" + field + '_'+ str(k-2) + '.dat', format = 'ascii')          #file in which the data for a given star is written
    

#********************************
#Part C2:

#The following code will do the following action:
#1. Open each data file, find the column for p , extract p for each of the epochs, and find the mean and the standard deviations. Can be repeated for other parameters.
#**********************************

#The following are two tables that will be created to act as catalogue and candidates table 

catalog = Table(names = ('Object', 'X', 'Y', 'RA', 'Dec', 'pol_median','pol_width','median_sigp','Theta_median','Theta_width','Theta_sigp_median','mag_median','mag_width','sig_mag_median','Nos_Epochs','p_ratio','m_ratio','t_ratio', 'potential' ),dtype=('S32','f16', 'f16', 'f16', 'f16','f16', 'f16', 'f16','f16','f16','f16','f16','f16','f16','f16','f16','f16','f16','S16'))

candidates = Table(names=('Object', 'X', 'Y', 'RA', 'Dec', 'pol_median','pol_width','median_sigp','theta_median','theta_width','theta_sigp_median','mag_median','mag_width','sig_mag_median','Nos_Epochs','p_ratio','m_ratio','t_ratio' ), dtype=('S32','f16','f16','f16','f16','f16', 'f16','f16','f16','f16','f16','f16','f16','f16','f16','f16','f16','f16'))



os.chdir(analysis_dir)
print os.getcwd()
table_files = glob2.glob('*.dat')   #lists all tables for stars 
for q,w in enumerate(table_files):
    print q, w


for k in range(len(table_files)):
    tabe = Table.read(table_files[k], format = 'ascii')           #open each table one by one
    if len(tabe['p']) >=5:                    #minimum no of obsevations required
        pol_median = numpy.median(tabe['p'])  #median of polarization
        pol_width = numpy.std(tabe['p'])      #width of the polarization measurement
        median_sigp = numpy.median(tabe['sig_p'])  #median of the polarization measurement uncertainity
        sigp_width = numpy.std(tabe['sig_p'])
        RA = numpy.median(tabe['RA'])
        Dec = numpy.median(tabe['Dec'])
        X = numpy.median(tabe['X-coord'])
        Y = numpy.median(tabe['Y-coord'])
        theta_median = numpy.median(tabe['theta'])
        theta_width = numpy.std(tabe['theta'])
        theta_sig_median = numpy.median(tabe['sig_theta'])
        mag_median = numpy.median(tabe['mag'])
        mag_width = numpy.std(tabe['mag'])
        median_sig_mag = numpy.median(tabe['sig_mag'])
        ID = table_files[k]
        ID = ID[0:-4]
        #to catch only candidates with non variable p and mag:
        P_Ratio = float(pol_width)/float(median_sigp)
        M_Ratio = float(mag_width)/float(median_sig_mag)
        T_Ratio = float(theta_width)/float(theta_sig_median)
        #print P_Ratio, M_Ratio
       
        if P_Ratio<= 1.2 and P_Ratio >= 0.9:
            if M_Ratio<= 1.2 and M_Ratio >= 0.9:
                catalog.add_row([ID, X, Y, RA, Dec, pol_median, pol_width, median_sigp,theta_median ,theta_width ,theta_sig_median,mag_median,mag_width,median_sig_mag, len(tabe['p']), P_Ratio, M_Ratio, T_Ratio,str('Yes')])
                candidates.add_row([ID,X, Y, RA, Dec, pol_median, pol_width, median_sigp, theta_median ,theta_width ,theta_sig_median,mag_median, mag_width, median_sig_mag, len(tabe['p']), P_Ratio, M_Ratio,T_Ratio])
                print '********************************got a candidate************************************************', ID 

        else:
            catalog.add_row([ID, X, Y, RA, Dec, pol_median, pol_width, median_sigp, theta_median ,theta_width ,theta_sig_median,mag_median, mag_width, median_sig_mag, len(tabe['p']),P_Ratio, M_Ratio, T_Ratio,str('No')])

catalog.write('catalog.dat', format = 'ascii')

candidates.write('candidates.dat', format = 'ascii')


print "JoB Done"
##end of code     





