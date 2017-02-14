from matplotlib import pyplot as py
from matplotlib import pylab 
import numpy as np
import os

from astropy.table import Table
import os

# Go to the directory where the results are stored.

candidate_dir = "/media/user/Seagate Backup Plus Drive/DATA/RoboPol/Candidates"

catalog = os.path.join(candidate_dir,"catalog")

if not os.path.exists(catalog):
    os.mkdir(catalog)

Star_catalog = "/media/user/Seagate Backup Plus Drive/DATA/RoboPol/RoboPol_Stars"


os.chdir(candidate_dir)
print os.getcwd()


candidate_list = Table.read("catalog.dat", format='ascii')

for k in range(len(candidate_list)):

    details = candidate_list[k]
    print details[0]
    field = details[0].split("_")[0]
    q_mean = details[5]
    u_mean = details[8]
    q_ratio = details[15]
    u_ratio = details[16]
    p_mean = details[3]
    Theta = details[4]
    RA = details[1]
    Dec = details[2]
    os.chdir(os.path.join(Star_catalog, field))
    st = Table.read(details[0] + ".dat",format='ascii')
    p = 100*st['p']
    p_mean = 100*np.mean(st['p'])
    
    #print p
    e_p = 100*st['error_p']
    no = range(len(st))
    #print no 
    q = 100*st['q']
    #print q
    u = 100*st['u']
    #print u
    e_q = 100*st['error_q']
    e_u = 100*st['error_u']
    mag = np.mean(st['mag'])
   
    #if p_mean >= 0.7: 

    py.gca().set_position((0.3,0.3,0.6,0.6))
    py.subplot(2, 1, 1)
    #py.title( "q_ratio= " + str(q_ratio))
    py.plot(no,q,'o-')
    py.errorbar(no,q,yerr=e_q,color='blue')
    py.xlim(-1, len(q))
    py.ylabel('q%')
    py.grid(True)
#    py.xticks
    
    py.subplot(2, 1, 2)
    #py.title( )
    po = py.plot(no,u,'o-')
    py.errorbar(no,u,yerr=e_u,color='black')
    py.ylabel('u%')
    py.xlim(-1, len(q))
    py.grid(True)
    py.xlabel('Epoch No')


#    py.subplot(3,1,3)
#    py.plot(no,p,'o-')
#    py.errorbar(no,p,yerr=e_p)
#    py.xlim(-1, len(q))
#    py.ylabel('p%')
#    py.grid(True)
#    py.xlabel('Epoch No')

    py.suptitle(" RA=" + str(RA) +  ", Dec=" + str(Dec)+"\n" +  "avg_p=" + str(p_mean)[:3] +"%" + ", Magnitude=" +str(mag)[:4]+"\n"+"q_ratio= " + str(q_ratio)+ " ,"+"u_ratio=" +str(u_ratio), fontsize=10, color='green')

    #text1 = , "<u> =",u_mean, "<p>=", p_mean, "Theta=", Theta) 
    #text2 = "q_ratio=", q_ratio, "u_ratio =", u_ratio
    #extra = Rectangle((0, 0), 1, 1, fc="w", fill=False, edgecolor='none', linewidth=0)
    #py.legend(["thadhis"], loc='upper left', title='Legend')
    

    #py.savefig(candidate_dir+"/" + details[0]+".pdf", format='pdf')

    py.savefig(catalog+"/"  + details[0] +".png", format='png')
    py.clf()


   


