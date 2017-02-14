import os, shutil 
from pipeline import robopol_pipeline
import glob  

#**********************************************
# Task: Analysis of the image files to get polarization data for all epochs of a blazar field.
#1. Go the directory where the blazar data is stored.
#2. Make a list of all the epoch directories within it.
#3. Enter the epoch folder, make a list of the fits files, and feed to the pipeline.
#4. Repeat step 3 for all the epochs of the Blazar.
#**********************************************



blazar_list = ['RBPLJ0211+1051']

def pol_measurement(blazar):                                #This is the function that will do all the tasks 1,2,3,4.

    # Input is Name of the field. eg. blazar = 'RBPLJ1048+7143' 

    print "Start of Polarization analysis of the field :", blazar

    #I have stored the data field wise using the program All_fields_data_extraction.py in the directory Fields of the Hard Drive as given in the path below.
    #Go to the directory where all the raw data of the RoboPol field is stored. 
    Blazar_Dir = os.path.join("/media/user/Seagate Backup Plus Drive/DATA/RoboPol/Fields" ,blazar)
    os.chdir(Blazar_Dir) 

    print "Now in the", os.getcwd() ,"directory" 

    Epochs = os.listdir(Blazar_Dir)               #List of the epochs(directories)

    for a, b in enumerate(Epochs):              #prints the list of epochs for the object
        print a ,b

    #Create a Directory where the o/p reduced data will be stored for all the epochs of the field:
    Data_Dir = "/media/user/Seagate Backup Plus Drive/DATA/RoboPol/Photom4/" + blazar 
    if not os.path.exists(Data_Dir):       
        os.mkdir(Data_Dir)

    #now from the list of epochs in Epochs, enter each epoch_dir, make a list of fits files, and feed it to the pipeline.
    for l in range(len(Epochs)):
        os.chdir(Epochs[l])                         #enter the epoch-directory
        fits_files = glob.glob("*.fits")            #gives the content fits files of the directory in a list
        for e ,files in enumerate(fits_files):      #gives list of all the fits files for the night
            print e, files

        flats_location = '/media/user/Seagate Backup Plus Drive/DATA/RoboPol/Raw_Data/catalogs/flats/'       #location where all the flat fits files of RoboPol are located. Note that flat fields are available from 23/6/13 onwards.

        output_dir = "/tmp/"+ blazar    #make a temporary output directory of blazar field in /tmp directory. Other directory as o/p dir doesnot work. IDK why!
        if not os.path.exists(output_dir):
            os.mkdir(output_dir)

        output_dir = output_dir +"/" + Epochs[l]
        if not os.path.exists(output_dir):
            os.mkdir(output_dir)

        final_dir = os.path.join(Data_Dir,Epochs[l])  # place in hard drive where the data will be finally stored.
        
        bll = robopol_pipeline.robopol_image(name = blazar, fits_location =fits_files, stack_lib = 'alipy', photom_method = 4, band = "R", output_dir = output_dir, model_date = '2014_04_30',bias =562, reduce_field = True,flat_dir = flats_location,remove_cr_flag = True)
     
        # Calculate polarization results
        bll.reduce_polarization()
             
        shutil.move(output_dir, final_dir)   #move files from temp directory to final directory.
        
        os.chdir(final_dir)
        items1 = glob.glob("*"+blazar + "*.fits")
        items2 = glob.glob("astrometry"+ "*")
        items3 = glob.glob("spot*.fits")
        items4 = glob.glob("spot*.cat")
        items = items1 + items2 + items3 + items4
        #list of objects to remove from the data dir, unnecessary space is used by these
        for j in items:
            os.remove(j)
        
        print "Polarization for epoch no", l,"over."

        os.chdir(Blazar_Dir)          #Go back to start position so that loop can function properly.

    print "Polarization Analysis of the field", blazar,"Done"



for k in range(len(blazar_list)):   #list fo blazars for which to carry out pipeline analysis.
    pol_measurement(blazar_list[k])





##end of code     

#Code revised on 7 Feb, 2017.






