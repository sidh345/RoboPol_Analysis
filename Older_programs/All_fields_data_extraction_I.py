import os, shutil 
import numpy as np
from pipeline import robopol_pipeline
import math
import subprocess
import sys
import glob2  #has recursive atribute that simple glob does not have
import pyfits
from astropy.table import Table
"""
part A: Steps:
    1. Load the names of all the fields from a txt file.
    2. Define a function that will do the following:
    a. Take the name of the RBPL field as input.
    b. Find all the science images of an object.
    c. Copy them to a seperate directory for each night, inside a directory for the field.
    d. Write the field name and the corresponding no of epochs it has been observed as an astropy table 
"""

def Get_Field_Images(blazar):
    #main data directory, will have to edited when used on a different m/c.
    os.chdir("/media/user/Seagate Backup Plus Drive/DATA/RoboPol/Fields") 
   
    #Create a directory where all the images of the blazar are going to be temporarily stored

    Blzr_DIR = os.path.join(os.getcwd(), blazar) 
    if not os.path.exists(Blzr_DIR):
        os.mkdir(Blzr_DIR)
    print os.path.basename(Blzr_DIR), "created"

    #go to the directory where all the raw data of RoboPOl is stored
    os.chdir("/media/user/Seagate Backup Plus Drive/DATA/RoboPol/Raw_Data/data/")

    print "Starting collection and storing science images of", blazar

    #The following codes search for images of the field in the hard drive, makes a list, and copies to a folder in the hard disk titled with the field_name/night

    images = glob2.glob("*/*/*" + blazar + "*_I_*.fits")      # "year/night/something" + blazar + "something"
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
    print "Observed no. of epochs:",len(epochs)
    t.add_row([blazar,len(epochs)])



if not os.path.exists("/media/user/Seagate Backup Plus Drive/DATA/RoboPol/Fields"):
    os.mkdir("/media/user/Seagate Backup Plus Drive/DATA/RoboPol/Fields")

t = Table(names=('Field','Observed_No_of_Epochs'),dtype=('S32','i4'))

all_fields = np.loadtxt("Fields_list.txt",'string')

for a,b in enumerate(all_fields):
    print a,b
    
for k in range(len(all_fields)):
    Get_Field_Images(all_fields[k])

t.write('Fields_Data_I.dat', format='ascii')
print t
print "JoB Done"
##end of code     




