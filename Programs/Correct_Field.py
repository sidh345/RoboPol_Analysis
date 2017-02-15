"""
***************************************************************************************************
Q. What am I trying to do with this code?

Go to the o/p directory of reduced field(output data of pipeline for any RoboPol field). For each night/epoch of observation, there is a csv file containing all the main data.
Collect all these data.csv files, and on each of them do the following operation:

    1. Find objects affected by any of the systematics of RoboPol(flat errors due to dust specks, nearby object contamination, Sextractor flagged objects etc).

    2. For all objects, make an astropy table. Clean objects will have boolean value True and and contaminated objects will have False. Also write with the objetctheir important parameters, which I will use with further codes for finding standard stars.

***************************************************************************************************
"""


from astropy.table import Table
import numpy as np
import math
import glob
import glob2
import os
import math


def Flags(f):


# for more info on this peice of code, refer to the program making_flat_histograms.py. This bit of code appends all the objects (by their serial no in the data.csv file beginning from 0) affected by any of the systematics of RoboPol system. The output is a list of bad objects. The remaining objects are then collected in an astropy table with their corresponding measured values for that epoch by subsequent codes(not this function).


    # The following two lines are commented out as they are already performed by the function which will employ this function, see lines 140-142.

    #data = open(data_file, 'r')  # open the csv data file
    #f = data.readlines()         #extract all the rows of data as collection of strings

    
    #First task is to find list of objects affected by flat field errors. This uses methods employed by Gina in her 2015 paper to flag out objects that appear to be affected by dust specks.
   
   #define empty lists to collect the data of required parameters. To know about what these lists refer to, look at Gina's paper.

    Del_F_h = []                             #Difference in flux of horizontal spots
    Del_F_v = []                             #Difference in flux of vertical spots
    Del_sig_F_h = []                         #Difference in standard deviation of flux of horizontal spots
    Del_sig_F_v = []                         #Difference in standard deviation of flux of vertical spots
    min_sig_F = []                           #Minimum value of  standard deviation of flux among the four spots
    max_sig_F = []                           #Maximum value of  standard deviation of flux among the four spots
    object_no = []                           #Serial no of object, starting from 0(the pythonic way)
    nearby_object_flag = []                  #Is there a close object nearby? if yes, list of such objects.
    SE_flag = []                             #Sextractor flags referring to various possible contaminations. Should be 0. if no, list of such objects.
    p_missing = []                           #Is p value missing in the data csv file. if yes, list of such objects.


    for k in range(3,len(f)):        #the first three lines contain verbose imformation 
        b = f[k].split(",")          #split the string into a list of different parameter entries. As it is a csv file, the entries are seperated by comma.
        F0 = float(b[26])
        sig_F0 = float(b[27])
        F1 = float(b[28])
        sig_F1 = float(b[29])
        F2 = float(b[30])
        sig_F2 = float(b[31])
        F3 = float(b[32])
        sig_F3 = float(b[33])

        # The following six are the quantities defined in Gina's paper as most robust to find dust contaminated stars. The labels (0,1) and (2,3) are the horizontal and vertical pairs of spots(which one is horizontal or vertical does not make any difference). 
        Del_F_h.append(abs(F0 - F1))  #taking absolute values as sign diff has no physical implications, but would increase the standard deviation estimates 
        Del_F_v.append(abs(F2 - F3))
        Del_sig_F_h.append(abs(sig_F0 - sig_F1))
        Del_sig_F_v.append(abs(sig_F2 - sig_F3))
        min_sig_F.append(min(sig_F0, sig_F1, sig_F2, sig_F3))
        max_sig_F.append(max(sig_F0, sig_F1, sig_F2, sig_F3))

        nearby_object = int(b[25])
        if nearby_object == 1:
            nearby_object_flag.append(k-3)              #So the list can start from 0th object.

        SE_flag_value = int(b[24])                      #This flag I may take off, depending on trail and error.
        if SE_flag_value != 0:
            SE_flag.append(k-3)

        p = float(b[4])
        if math.isnan(p) == True:                              #if p is missing, it will be written as nan, so checking if that is so in this line
            p_missing.append(k-3)

        object_no.append(k-3)  #serial no of all objects in field starting from 0, will be used to make a dictionary to uniquely tag all values.


    #Simplifying the name of the six parameter lists, ie re-naming them for easier coding in the following lines.

    A = Del_F_h
    B = Del_F_v
    C = Del_sig_F_h
    D = Del_sig_F_v
    E = min_sig_F 
    F = max_sig_F 

    problem_obj= []    #list that will contain all falt flagged object ids

    parameter_lists = [A,B,C,D,E,F]  #make a list of all paremeter lists

    for i in range(len(parameter_lists)):

        data = parameter_lists[i]          #take one parameter list at a time.

        #make temperory dictionaries to map each object to it's parameter value

        dict_temp = dict(zip(object_no, data))

        #caluclate the mean and the standard deviation of the distribution.
        mean = np.mean(data)
        sigma = np.std(data)
        for l in set(data):               #used a set filter to reduce repeated computations required for values repeated in the parameter set.   
            if (float(l) - float(mean)) >= (2*sigma + mean):       # criterion for selecting outliers
                #print "got an outlier", l
                for (e,f) in dict_temp.iteritems():   #dict_temp is the temporary dictionary I created. iteritems can be used for reverse mapping, so used here.
                    if  l == f:
                        problem_obj.append(e)       # append the object no to this list


    print "No of Flat error objects", len(set(problem_obj))

    flagged_objects = list(set(problem_obj + nearby_object_flag + p_missing + SE_flag))  
    print "Total no of flagged objects is", len(flagged_objects)

    return flagged_objects


def Make_Table(data_file):

    #data_file = "/home/user/Dropbox/data.csv"

    f = open(data_file,"r")

    b = f.readlines()

    print "Total no of objects in the field = ", (len(b)-3)

    # make an astropy table that will conatin data for all fair objects in the field.
    tabl = Table(names=(['X-coord', 'Y-coord', 'RA', 'Dec','p','error_p', 'q', 'error_q', 'u', 'error_u', 'mag', 'error_mag','Theta','Fair_Object']), dtypes=('f8','f8','f8','f8','f8','f8','f8','f8','f8','f8','f8','f8','f8','f8'))

    flag = Flags(b)   #will generate the list of flagged objects

    f.close()

    all_list = range(len(b)-3)

    good_list = [x for x in range((len(b))-3) if x not in flag]    #List of fair objects in the epoch. (len(b)-3) is total no of objects in the csv file.
    print "total no of fair objects in the field", (len(good_list))

    print "  "

    # Set of lines to add the parameter values of all objects to the astropy table. 
    for k in all_list:  
        if k in good_list:
            values = b[k+3].split(",")  #read the line b[k+3] and parse the field entries seperated by commas as it is csv file.
            value = values[:6] + values[8:12] + values[16:18] + values[6:7] + [True]  #possible because list concatenation preserves the order, like string concatenation.
            tabl.add_row(value)
        else:
            values = b[k+3].split(",")  #read the line b[k+3] and parse the field entries seperated by commas as it is csv file.
            value = values[:6] + values[8:12] + values[16:18] + values[6:7] + [False]  #possible because list concatenation preserves the order, like string concatenation.
            tabl.add_row(value)

        
    return tabl



def Correct_Fields(blazar):

    # eg. blazar = "RBPLJ1809+2041"
    #Data_directory = "/home/user/Desktop/" + blazar

    Data_directory = "/media/user/Seagate Backup Plus Drive/DATA/RoboPol/Photom4/" + blazar   #specific to blazar

    #OutPut_Directory = "/home/user/"

    OutPut_Directory = "/media/user/Seagate Backup Plus Drive/DATA/RoboPol/Corrected_Fields/"  # Directory where all corrected data will be stored

    OutPut_Dir = os.path.join(OutPut_Directory, blazar)
    if not os.path.exists(OutPut_Dir):                #make a directory to contain all the analysis files for a field
            os.mkdir(OutPut_Dir)

    os.chdir(Data_directory)
    print "**Now in**", os.getcwd()

    csv_files = glob2.glob("*/data.csv")              #list of data.csv files of all the epochs

    no_epochs = len(csv_files)

    for k in range(no_epochs):                       #operation for each csv file
        epoch = csv_files[k].split("/")
        epoch = epoch[0]                             #to get the epoch 
        output_table = Make_Table(csv_files[k])      #generates a clean table for that epoch
        output_table.write(OutPut_Dir + "/" + epoch + ".dat", format='ascii')  #writes it to dat file with the epoch name as file name
        #print output_table

    print "Clean tables generated for the field: ", blazar



blazars = os.listdir("/media/user/Seagate Backup Plus Drive/DATA/RoboPol/Photom4/")  #list of fields reduced by the pipeline
corrected_fields = os.listdir("/media/user/Seagate Backup Plus Drive/DATA/RoboPol/Corrected_Fields/")  #already corrected fields

blazar_list = [x for x in blazars if x not in corrected_fields] #list of blazars that need to be corrected


for blazar in blazar_list:
    a =  Correct_Fields(blazar)
print "job done"

#I have gone through the revision and verification of code. 3/2/2017.
#Revised again on 7/2/2017 and 8/2/2017.
#Revised again on 15 February to add boolean character for bad fields.







