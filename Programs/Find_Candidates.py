import glob2
from astropy.table import Table
import numpy
import os, shutil


"""

This code will do the following action:

1. Go to the directory called RoboPol_Stars where each object with it's all fair readings are kept Field wise.

2. Go to the blazar directory inside Stars directory.

3. Open astropy table dat file of each star, find the column for q , extract q for each of the epochs, and find the mean and the standard deviations. Can be repeated for other parameters like u and magnitude.

"""

#Candidate dir is the directory where the candidates list in an astropy table is going to be kept.
Candidate_Dir = os.path.join("/media/user/Seagate Backup Plus Drive/DATA/RoboPol/", "Candidates")
if not os.path.exists(Candidate_Dir):
    os.mkdir(Candidate_Dir)

#Directory where all the RoboPol stars in astropt table format are kept.
Star_Catalog_Dir = "/media/user/Seagate Backup Plus Drive/DATA/RoboPol/RoboPol_Stars"
os.chdir(Star_Catalog_Dir)
print os.listdir(os.getcwd())


#criterion for selecting a good candidate. Should be visible in at least 5 epochs with good snr measurement.
R = 1.3                                                         #The magic ratio for candidates
Min_Epochs = 5



#The following are two tables that will be created to act as catalogue and candidates table. The catalogue table will contain data about potential candidates as well as those that are not. 

catalog = Table(names = ('Object','RA', 'Dec', 'p', 'Theta', 'q_med','q_width','q_terror','u_med','u_width','u_terror','mag_med','mag_width','mag_terror','Nos_Epochs','q_ratio','u_ratio', 'm_ratio','potential' ),dtype=('S32','f4', 'f4', 'f4', 'f4', 'f4','f4', 'f4', 'f4', 'f4','f4','f4','f4','f4','f4','f4','f4','f4','S16'))

candidates = Table(names=('Object', 'RA', 'Dec', 'p','Theta','q_med','q_width','q_terror','u_med','u_width','u_terror','mag_med','mag_width','mag_terror','Nos_Epochs','q_ratio','u_ratio','m_ratio'), dtype=('S32','f4','f4','f4','f4','f4','f4', 'f4','f4','f4','f4','f4','f4','f4','f4','f4','f4','f4'))



table_files = glob2.glob('*/*.dat')   #lists all tables for stars for all blazar fields

print "Total no of RoboPol Stars:", len(table_files)

for k in table_files:
    tabe = Table.read(k, format = 'ascii')           #open each table one by one

#    ad = []                                          # a list to contain the row no of the table that do not satisfy the SNR criterion
#    for n in range(len(q)):                        #collects data for each row of the table
#        if p[n]/error_p[n] <= SNR:
#            ad.append(n)
#    tabe.remove_rows(ad)                             #remove the rows from the table.
            
    if len(tabe['p']) >= Min_Epochs:                    #minimum no of obsevations required
        p = numpy.median(tabe['p'])

        Theta = numpy.median(tabe['Theta'])

        q_median = numpy.median(tabe['q'])  #median of qarization
        q_width = numpy.std(tabe['q'])      #width of the qarization measurement
        median_sigq = numpy.median(tabe['error_q'])  #median of the qarization measurement uncertainity
        
        RA = numpy.median(tabe['RA'])
        Dec = numpy.median(tabe['Dec'])

        X = numpy.median(tabe['X-coord'])
        Y = numpy.median(tabe['Y-coord'])
        
        u_median = numpy.median(tabe['u'])
        u_width = numpy.std(tabe['u'])
        median_sigu = numpy.median(tabe['error_u'])
        
        mag_median = numpy.median(tabe['mag'])
        mag_width = numpy.std(tabe['mag'])
        median_sig_mag = numpy.median(tabe['error_mag'])
        
        ID = k  #Name of the robopol star
        ID =(ID.split("/"))[1]
        ID = ID[0:-4]

        #to catch only candidates with non variable p and mag:
        Q_Ratio = float(q_width)/float(median_sigq)
        M_Ratio = float(mag_width)/float(median_sig_mag)
        U_Ratio = float(u_width)/float(median_sigu)
        
       
        if Q_Ratio<= R and U_Ratio<= R and p<= 0.04: 
            catalog.add_row([ID, RA, Dec, p,Theta, q_median, q_width, median_sigq,u_median ,u_width ,median_sigu,mag_median,mag_width,median_sig_mag, len(tabe['q']), Q_Ratio, U_Ratio, M_Ratio, str('Yes')])
            candidates.add_row([ID, RA, Dec, p, Theta, q_median, q_width, median_sigq,u_median ,u_width ,median_sigu,mag_median,mag_width,median_sig_mag, len(tabe['q']), Q_Ratio, U_Ratio, M_Ratio ])
            print '********************************got a candidate************************************************', ID 

        else:
            catalog.add_row([ID, RA, Dec, p, Theta, q_median, q_width, median_sigq,u_median ,u_width ,median_sigu,mag_median,mag_width,median_sig_mag, len(tabe['q']), Q_Ratio, U_Ratio, M_Ratio, str('No')])


catalog.write(Candidate_Dir + '/' +'catalog.dat', format = 'ascii')

candidates.write(Candidate_Dir + '/' + 'candidates.dat', format = 'ascii')

print "JoB Done"

#code revised and reviewed on 3 Feb/2017.
#code reviewed on 8 Feb, 2017. No change.
##end of code 
