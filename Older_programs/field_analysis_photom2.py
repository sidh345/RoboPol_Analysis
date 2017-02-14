import os, shutil 
from pipeline import robopol_pipeline
import glob  

#**********************************************
# PART B: Analysis of the image files to get polarization
#1. Go the directory where the blazar data is stored.
#2. Make a list of all the directories within it: list of directories named on the epochs.
#3. Enter the epoch folder, make a list of teh fits files, and feed to the pipeline.
#4. Repeat step 3 for all the epochs of the Blazar.
#**********************************************


blazar_list = ['RBPLJ2334+0736']    #'RBPLJ2022+7611']



def pol_measurement(blazar): 
    # Name of the target field
    #blazar = 'RBPLJ1048+7143' 
    print "Start of Polarization analysis of fields of the", blazar

    #main data directory, will have to edited when used on a different m/c.
    #go to the directory where all the raw data of the RoboPol filed is stored

    Blazar_Dir = os.path.join("/media/user/Seagate Backup Plus Drive/DATA/RoboPol/Fields" ,blazar)
    os.chdir(Blazar_Dir) 

    print "Now in the", os.getcwd() ,"directory" 

    Epochs = os.listdir(Blazar_Dir)               #List of the epochs(directories)

    for a, b in enumerate(Epochs):              #prints the list of epochs for the object
        print a ,b

    #Create a Directory where the o/p data will be stored for all the epochs:
    Data_Dir = "/media/user/Seagate Backup Plus Drive/DATA/RoboPol/Flat_fielded_photom2/" + blazar #+ "_flat_cr_corrected"
    if not os.path.exists(Data_Dir):       
        os.mkdir(Data_Dir)

    #now from the list of epochs in Epochs, enter each epoch_dir, make a list of fits files, and feed it to the pipeline.
    for l in range(26) and range(27,len(Epochs)):
        os.chdir(Epochs[l])                       #enter the epoch-directory
        fits_files = glob.glob("*.fits")           # gives the content of the directory in a list
        for e ,files in enumerate(fits_files):      #gives list of all the fits files for the night
            print e, files

        flats_location = '/media/user/Seagate Backup Plus Drive/DATA/RoboPol/Raw_Data/catalogs/flats/'       #location where all the fits files of RoboPol are located. Note that flat fields are available from 23/6/13 onwards.

        output_dir = "/tmp/"+ blazar  
        if not os.path.exists(output_dir):
            os.mkdir(output_dir)

        output_dir = output_dir +"/" + Epochs[l]
        if not os.path.exists(output_dir):
            os.mkdir(output_dir)

        final_dir = os.path.join(Data_Dir,Epochs[l])
        
        if not os.path.exists(output_dir):
            os.mkdir(output_dir)

        bll = robopol_pipeline.robopol_image(name = blazar, fits_location =fits_files, stack_lib = 'alipy', photom_method = 2, band = "R", output_dir = output_dir, model_date = '2014_04_30',bias =562, reduce_field = True,flat_dir = flats_location,remove_cr_flag = True)
     
        # Calculate polarization results
        bll.reduce_polarization()
             
        shutil.move(output_dir, final_dir)
        print "Polarization for epoch no", l,"over."
        
        os.chdir(final_dir)
        items1 = glob.glob("*"+blazar + "*.fits")
        items2 = glob.glob("astrometry"+ "*")
        items3 = glob.glob("spot*.fits")
        items4 = glob.glob("spot*.cat")
        items = items1 + items2 + items3 + items4
        #list of objects to remove from the data dir, unnecessary space is used by these
        for j in items:
            os.remove(j)
        
        os.chdir(Blazar_Dir)          #Go back to start position so that loop cn function properly.

    print "Polarization Analysis of the field", blazar,"Done"


for k in range(len(blazar_list)):
    pol_measurement(blazar_list[k])

##end of code     






