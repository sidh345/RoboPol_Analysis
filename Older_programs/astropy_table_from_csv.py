"""
***************************************************************************************************
Q. What am I trying to do with this code?

Go to the o/p directory of reduced field, collect all the data csv files, and on each of them do the following operation:

    1. Find objects affected by any of the systematics of RoboPol.

    2. For all other objects, make an astropy table which will have only clean objects and their important parameters that I will use for finding standard stars.

***************************************************************************************************
"""


from astropy.table import Table
import matplotlib.pyplot as plt
from collections import Counter,OrderedDict
import numpy as np
import math
import glob
import glob2
import os



def Flags(f):

    # for more info on this peice of code, refer to the program making_flat_histograms.py.
    # This bit of code appends all the objects (by their serial no in the data.csv file beginning from 0) affected by any of the systematics of RoboPol system.
    # The output is a list of objects. 
    

    #data = open(data_file, 'r')  # open the data file
    #f = data.readlines()         #extract all the rows of data as collection of strings
    #define empty lists to collect the data of required parameters

    Del_F_h = []
    Del_F_v = []
    Del_sig_F_h = []
    Del_sig_F_v = []
    min_sig_F = []
    max_sig_F = []
    object_no = []
    nearby_object_flag = []
    #photometry_flag = []
    p_missing = []


    for k in range(3,len(f)):        #the first three lines contain verbose imformation 
        b = f[k].split(",")          #split the string into componenets for different field entries
        F0 = float(b[26])
        sig_F0 = float(b[27])
        F1 = float(b[28])
        sig_F1 = float(b[29])
        F2 = float(b[30])
        sig_F2 = float(b[31])
        F3 = float(b[32])
        sig_F3 = float(b[33])

        nearby_object = int(b[25])
    #    photometry_ok = int(b[15])

        if nearby_object == 1:
            nearby_object_flag.append(k-3)

    #    if photometry_ok == 0:
    #        photometry_flag.append(k-3)


        p = float(b[4])
        if math.isnan(p) == True:
            p_missing.append(k-3)

            
        Del_F_h.append(abs(F0 - F2))   #taking absolute values as sign difference has no physical implications, but would increase the standard deviation estimates 
        Del_F_v.append(abs(F1 - F3))
        Del_sig_F_h.append(abs(sig_F0 - sig_F2))
        Del_sig_F_v.append(abs(sig_F1 - sig_F3))
        min_sig_F.append(min(sig_F0, sig_F1, sig_F3, sig_F0))
        max_sig_F.append(max(sig_F0, sig_F1, sig_F3, sig_F0))

        object_no.append(k-3)  #will be used to make a dictionary to uniquely tag all values

    A = Del_F_h
    B = Del_F_v
    C = Del_sig_F_h
    D = Del_sig_F_v
    E = min_sig_F 
    F = max_sig_F 
    Object_Id = object_no

    problem_obj= []    #list that will contain all flagged object ids

    parameter_lists = [A,B,C,D,E,F]  #make a list of all paremeter lists

    for i in range(len(parameter_lists)):

        data = parameter_lists[i]

        #make temperory dictionaries to map each object to it's parameter value

        dict_temp = dict(zip(object_no, data))

        #caluclate the mean and the standard deviation of the distribution.
        mean = np.mean(data)
        sigma = np.std(data)
        #print "mean = ",mean ,", Standatd_deviation = ", sigma 
        for l in set(data):               #used a set filter to reduce repeated computations required for values repeated in the parameter set.   
            if l - mean >= 2*sigma:       # criterion for selecting outliers
                #print "got an outlier", l
                for (e,f) in dict_temp.iteritems():
                    if  l == f:
                        #print e,f
                        problem_obj.append(e)       # append the object no to this list




    print "No of Flat error objects", len(set(problem_obj))

    flagged_objects = list(set(problem_obj + nearby_object_flag +p_missing))  
    print "Total no of flagged objects is", len(flagged_objects)

    return flagged_objects




def make_table(data_file):

    #data_file = "/home/siddharth/Dropbox/data.csv"

    f = open(data_file,"r")

    b = f.readlines()

    print "Total no of objects in the field = ", (len(b)-3)

    Column_names = b[2].split(",")

    Column_names = Column_names[:3] + Column_names[8:12]+ Column_names[16:18]

    table = Table(names=(['X-coord', 'Y-coord', 'RA', 'Dec', 'q', 'sig_q', 'u', 'sig_u', 'mag', 'sig_mag']), dtypes=('f8','f8','f8','f8','f8','f8','f8','f8','f8','f8'))

    flag = Flags(b)

    #print "Total no of flagged objects in the field", len(flag)

    good_list = [x for x in range((len(b))-3) if x not in flag]
    print "total no of fair objects in the field", (len(good_list)-3)

    print "  "


    for k in good_list:
        values = b[k+3].split(",")
        values = values[:4] + values[8:12] + values[16:18]
        
        table.add_row(values)
        
    #print table

    return table



def Correct_Fields(blazar):


    #blazar = "RBPLJ1809+2041"

    Data_directory = "/home/siddharth/Desktop/" + blazar

    #Data_directory = "/media/siddharth/Seagate Backup Plus Drive/DATA/RoboPol/Photom4/" + blazar   #specific to blazar

    os.chdir(Data_directory)
    print "****************************************************Now in", os.getcwd()

    OutPut_Directory = "/home/siddharth/"

    #OutPut_Directory = "/media/siddharth/Seagate Backup Plus Drive/DATA/RoboPol/Corrected_Fields/"  

    OutPut_Dir = os.path.join(OutPut_Directory, blazar)
    if not os.path.exists(OutPut_Dir):                #make a directory to contain all the analysis files for a field
            os.mkdir(OutPut_Dir)


    csv_files = glob2.glob("*/data.csv")

    no_epochs = len(csv_files)

    for k in range(no_epochs):
        epoch = csv_files[k].split("/")
        epoch = epoch[0]
        output_table = make_table(csv_files[k])
        output_table.write(OutPut_Dir + "/" + epoch + ".dat", format='ascii')
        #print output_table


    print "Clean tables generated for the field: ", blazar



blazar = "RBPLJ1203+6031"

a =  Correct_Fields(blazar)










