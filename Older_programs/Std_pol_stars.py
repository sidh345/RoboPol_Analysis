import glob
from astropy.table import Table
import numpy
import os, shutil


"""
Part C2:

The code will do the following action:
1. Open each data file in the catalog directory, find the column for p , extract p for each of the epochs, and find the mean and the standard deviations. Can be repeated for other parameters like EVPA and magnitude.


2. Need to put in a cut off SNR for these fields. Open the astropy table, find the ratio of p/sigp and delete the rows which dont have the minimum cut off.  
"""

#The following are two tables that will be created to act as catalogue and candidates table. The catalogue table will contain data about potential candidates as well as those that are not. 

catalog = Table(names = ('Object', 'X', 'Y', 'RA', 'Dec', 'pol_median','pol_width','median_sigp','Theta_median','Theta_width','Theta_sigp_median','mag_median','mag_width','sig_mag_median','Nos_Epochs','p_ratio','t_ratio', 'm_ratio','potential' ),dtype=('S32','f4', 'f4', 'f4', 'f4','f4', 'f4', 'f4','f4','f4','f4','f4','f4','f4','f4','f4','f4','f4','S16'))

candidates = Table(names=('Object', 'RA', 'Dec', 'pol_median','median_sigp','theta_median','sigt_median','mag_median','sigm_median','Nos_Epochs','p_ratio','t_ratio','m_ratio'), dtype=('S32','f4','f4','f4','f4','f4','f4','f4','f4','f4','f4','f4','f4'))


Catalog_Dir = "/media/siddharth/Seagate Backup Plus Drive/DATA/RoboPol/Catalog"

os.chdir(Catalog_Dir)

table_files = glob.glob('*.dat')   #lists all tables for stars 

print "Total no of RoboPol Stars:", len(table_files)

Q = 1.5                                                             #The magic ratio for candidates

for k in range(len(table_files)):
    tabe = Table.read(table_files[k], format = 'ascii')           #open each table one by one
    #print len(tabe), tabe
    pol = tabe['p']
    error_pol = tabe['sig_p']
    ad = []                                          # a list to contain the row no of the table that do not satisfy the SNR criterion
    for n in range(len(pol)):                        #collects data for each row of the table
        if pol[n]/error_pol[n] <= 3.0:
            ad.append(n)
    tabe.remove_rows(ad)                             #remove the rows from the table.
            

    if len(tabe['p']) >=15:                    #minimum no of obsevations required
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
       
        if P_Ratio<= Q and T_Ratio<= Q: 
            catalog.add_row([ID, X, Y, RA, Dec, pol_median, pol_width, median_sigp,theta_median ,theta_width ,theta_sig_median,mag_median,mag_width,median_sig_mag, len(tabe['p']), P_Ratio, T_Ratio, M_Ratio,str('Yes')])
            candidates.add_row([ID, RA, Dec, pol_median, median_sigp, theta_median ,theta_sig_median,mag_median, median_sig_mag, len(tabe['p']), P_Ratio,T_Ratio, M_Ratio])
            print '********************************got a candidate************************************************', ID 

        else:
            catalog.add_row([ID, X, Y, RA, Dec, pol_median, pol_width, median_sigp, theta_median ,theta_width ,theta_sig_median,mag_median, mag_width, median_sig_mag, len(tabe['p']),P_Ratio, T_Ratio, M_Ratio, str('No')])

Candidate_Dir = os.path.join(Catalog_Dir, "Candidates")

if not os.path.exists(Candidate_Dir):
    os.mkdir(Candidate_Dir)


catalog.write(Candidate_Dir + '/' +"Q=" + str(Q)+'catalog.dat', format = 'ascii')

candidates.write(Candidate_Dir + '/' +"Q=" + str(Q)+ 'candidates.dat', format = 'ascii')

print "JoB Done"
##end of code 
