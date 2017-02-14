from matplotlib import pyplot as py
from matplotlib import pylab 
import numpy as np
from astropy.table import Table
import os
import datetime


# Go to the directory where the results are stored.
candidate_dir = "/media/user/Seagate Backup Plus Drive/DATA/RoboPol/Candidates"
#directory where star tables are stored.
Star_catalog = "/media/user/Seagate Backup Plus Drive/DATA/RoboPol/RoboPol_Stars"

os.chdir(candidate_dir)
print os.getcwd()

candidate_tab = Table.read("candidates.dat", format='ascii') 

for k in range(len(candidate_tab)):

    details = candidate_tab[k]  #read one candidate at a time, this is an astropy table row
    print details[0]
    field = details[0].split("_")[0]
    q_mean = details[5]
    u_mean = details[8]
    q_ratio = details[15]
    u_ratio = details[16]
    p_mean = 100*details[3]
    Theta = details[4]
    RA = details[1]
    Dec = details[2]
    mag = details[11]

    os.chdir(os.path.join(Star_catalog, field))  #go to the directory where the candidate star table is located
    st = Table.read(details[0] + ".dat",format='ascii')  #open the table of the candidate star
       
    p = 100*st['p']   
    e_p = 100*st['error_p']
    no = range(len(st))
    q = 100*st['q']
    u = 100*st['u']
    e_q = 100*st['error_q']
    e_u = 100*st['error_u']
    m = st['mag']
    e_m = st['error_mag']

    Year = st['Year']
    Month = st['Month']
    Date = st['Date']
    

    JD = []
    for k in range(len(Date)):
        a = datetime.date(int(Year[k]),int(Month[k]),int(Date[k]))
        print a
        JD.append(a)

    print JD

    xmin = datetime.date(2013,06,01)
    xmax = datetime.date(2016,12,31)


    med_q = np.median(q)
    py.subplot(311)
    py.plot(JD,q,'ro',color='black')
    py.axhline(y=med_q,color='red',linestyle='--')
    py.errorbar(JD,q,yerr=e_q,linestyle='',color='blue')
    py.ylabel('q%')
    py.grid(True)
    py.xlim(xmin, xmax)


    """ 
    med_eq = np.median(e_q)
    py.subplot(322)
    py.plot(JD,e_q,'ro',color='gray')
    py.axhline(y=med_eq, linestyle='--',color='violet')
    py.ylabel('q_error',color='red')
    py.grid(True)
    py.tick_params(axis='y', which='both', labelleft='off', labelright='on')
    py.xlim(xmin, xmax)
    """
    med_u = np.median(u)
    py.subplot(312)
    py.plot(JD,u,'ro',color='black')
    py.axhline(y=med_u,color='red',linestyle='--')
    py.errorbar(JD,u,yerr=e_u,linestyle='',color='blue')
    py.ylabel('u%')
    py.xlim(xmin, xmax)
    py.grid(True)
    """
    med_eu = np.median(e_u)
    py.subplot(324)
    py.plot(JD,e_u,'ro',color='gray')
    py.axhline(y=med_eu,linestyle='--',color='violet')
    py.ylabel('u_error')
    py.grid(True)
    py.tick_params(axis='y', which='both', labelleft='off', labelright='on')
    py.xlim(xmin, xmax)
    """
    med_p = np.median(p)   
    py.subplot(313)
    py.plot(JD,p,'ro',color='black')
    py.axhline(y=med_p,color='red',linestyle='--')
    py.errorbar(JD,p,yerr=e_p,linestyle='',color='blue')
    py.ylabel('p%')
    py.grid(True)
    py.xlim(xmin, xmax)
    """
    py.subplot(326)
    py.plot(JD,e_p,'ro',color='gray')
    py.ylabel('p_error')
    py.grid(True)
    py.tick_params(axis='y', which='both', labelleft='off', labelright='on')
    py.xlim(xmin, xmax)
    """
    py.gcf().autofmt_xdate()

    
    py.suptitle(" RA=" + str(RA) +  ", Dec=" + str(Dec)+"\n" +  "avg_p=" + str(p_mean)[:3] +"%" + ", Magnitude=" +str(mag)[:4]+"\n"+"q_ratio= " + str(q_ratio)+ " ,"+"u_ratio=" +str(u_ratio),fontweight='bold', fontsize=10, color='red')
    #py.show()
    #py.savefig(candidate_dir+"/" + details[0]+".pdf", format='pdf')
    py.savefig(candidate_dir+"/" + details[0] +".png", format='png')
    py.clf()


#code reviewed and revised on 8/2/2017.   


