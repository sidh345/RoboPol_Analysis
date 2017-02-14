"""
***************************************************************************************************

Aim: To flag off objects affected by the following errors :
     a. Absence of p measurement.
     b. Nearby objects.
     c. Dust and bad optic affected:

Errors (a) and (b) can be found out by looking at the columns of p and nearby object flag in the data.csv file. 

To get the objects affected by error(c), the last eight columns of the data.csv file have to be used. How this is done is described below.


PART A: Find 

    To get the characteristics of the image apertures from flats of that night and flag off those objects that fall on regions of the image affected by dust, following steps are executed by the code:
    
1. Open the csv file and extract the quantities F and Sig_F for each of the four spots of an object.

2. Construct the six quantities mentioned in Gina's paper.

3. Find the mean and standard deviation for each of the quantities, and find outliers by using 2-sigma limit. Optionally, plot histograms of all these six components. 
 
4. Make a list of all these outliers for each of the parameters, make a overall list of outliers found for any of the six paparmeters.

Concatenate this list with the outlier list found for (a) & (b), and we get a list of all flagged objects for the field.

***************************************************************************************************

"""

import matplotlib.pyplot as plt
from collections import Counter,OrderedDict
import numpy as np
import math

#NULL = x(float('nan')


data_file = "/home/siddharth/Dropbox/data.csv"


data = open(data_file, 'r')  # open the data file

f = data.readlines()         #extract all the rows of data as collection of strings

print "total no of objects in the field", (len(f)-3)

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
        nearby_object_flag.append(k-2)

#    if photometry_ok == 0:
#        photometry_flag.append(k-2)


    p = float(b[4])
    if math.isnan(p) == True:
        p_missing.append(k-2)

        
    Del_F_h.append(abs(F0 - F2))   #taking absolute values as sign difference has no physical implications, but would increase the standard deviation estimates 
    Del_F_v.append(abs(F1 - F3))
    Del_sig_F_h.append(abs(sig_F0 - sig_F2))
    Del_sig_F_v.append(abs(sig_F1 - sig_F3))
    min_sig_F.append(min(sig_F0, sig_F1, sig_F3, sig_F0))
    max_sig_F.append(max(sig_F0, sig_F1, sig_F3, sig_F0))

    object_no.append(k-2)  #will be used to make a dictionary to uniquely tag all values

print "Extracted all data from the csv file"

print "Total", len(nearby_object_flag),"objects affected by nearby objects", nearby_object_flag 

print "Missing p values:", p_missing


"""   
print Del_F_h
print Del_F_v 
print Del_sig_F_h 
print Del_sig_F_v 
print min_sig_F 
print max_sig_F  
print object_no
"""

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
    print "mean = ",mean ,", Standatd_deviation = ", sigma 
    for l in set(data):               #used a set filter to reduce repeated computations required for values repeated in the parameter set.   
        if l - mean >= 2*sigma:       # criterion for selecting outliers
            print "got an outlier", l
            for (e,f) in dict_temp.iteritems():
                if  l == f:
                    print e,f
                    problem_obj.append(e)       # append the object no to this list

    print set(problem_obj)

"""
    #to plot the frequency plot of the different paramenters
     

    b = dict(Counter(data))
    c = sorted(b.keys())      # to get in increasing order


    x = []
    y = []

    for k in c:

        x.append(k)
        y.append(b[k])

    plt.plot(x,y,'ro')
    plt.show()

"""
print "list of objects affected by dust/optic errors", list(set(problem_obj))

flagged_objects = list(list(set(problem_obj)) + nearby_object_flag)

print "list of flagged objects is(Total= ", len(flagged_objects), ")", flagged_objects






