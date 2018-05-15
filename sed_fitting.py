import os,shutil,pylab,math,subprocess
import numpy as np
import astropy.units as u
import matplotlib.pyplot as plt
from fnmatch import fnmatch
from multiprocessing import cpu_count, Pool
from functools import partial
from astropy.units import astrophys
from astropy.table import Table,Column
from matplotlib import rc
from scipy import interpolate
from tqdm import tqdm

rc('text', usetex=True)
plt.rcParams['font.family'] = 'serif'
plt.rcParams['mathtext.fontset'] = 'dejavuserif'
plt.rcParams['text.usetex'] = True
plt.rcParams['text.latex.unicode'] = True

# options
directory = 'year4'
distance_in_kpc = 8
assumed_rgd = 200.0000

# set variables
targets = []
target_names = []

# solar constant = 1379 W
# distance to sun in kpd 4.8483E-9
distance_norm = math.log10((((int(distance_in_kpc)/4.8482E-9))**2)/1379)
min_norm = 1e-14
max_norm = 1e-10
ntrials = 1000
trials = np.linspace(min_norm,max_norm,ntrials)
latex_array=[]

for item in os.listdir('./visir_spectra/'):
    if fnmatch(item,"*flux_calibrated.txt"):
        targets.append('visir_spectra/'+item)
targets = ['visir_spectra/IRAS-17030-3053_flux_calibrated.txt']

try:
    f = open('gilgamesh_results.csv', 'r')
except IOError:
    f = open('gilgamesh_results.csv', 'w')
    f.write('source, luminosity, odep, scaled vexp, mdot \n')
    f.close()

# creates/removes files

def get_models(dir):
    models =[]
    for dd,_,files in os.walk(dir): # dd is the directory name _=throw away
        files = [f for f in files if fnmatch(f,'*.s*')] # removes .inp and .out files
        models.extend([dd+'/'+ll for ll in files]) # single within files
    return sorted(models)

def get_dusty(file):
    xv, yv = np.loadtxt(file, usecols=[0,1],unpack=True)
    return np.array(xv), np.array(yv)

def get_supp_data(file):
    supp_array = Table(np.genfromtxt(file,delimiter=',', names=True))
    xs = np.array(supp_array.columns[0])
    ys = np.array(supp_array.columns[1])
    ys = ys * u.Jy
    ys = ys.to(u.W/(u.m * u.m),equivalencies=u.spectral_density(xs * u.um))
    out_supp=np.array(list(zip(xs,ys.value)))
    return  out_supp


def get_dusty_outputs(dir):
    output_list = []
    for dd,_,files in os.walk('.'):
        outputs = [f for f in files if fnmatch(f, '*.out*')] # removes .inp and .out files
        output_list.extend([dd+'/'+ll for ll in outputs])
    return sorted(output_list)


def least2(data, model_vales):
    return np.square(model_vales - data).sum()


# this must stay here
pool = Pool(cpu_count() - 1)


def fit_norm(data, model_fname):
    model = trim(data,get_dusty(model_fname))
    list(model[1]*t for t in trials)
    stat_values = pool.map(partial(least2,data[1]), (model[1]*t for t in trials))
    return stat_values


def get_data(filename):
    x, y = np.loadtxt(filename, delimiter=',', unpack=1, skiprows=110)
    y = y * u.Jy
    y = y.to(u.W/(u.m * u.m), equivalencies=u.spectral_density(x * u.um))
    return x, np.array(y)


# tolerance of how close the values need to be in order to interpolate new value
tol = 1e-3


def resample(small,big,interp=3):
    # interp is the numrber of data points which the interp line is fit to (should be odd)
    sx,sy = small
    bx,by = big
    new_y = []
    closest = [abs(bx-x).argmin() for x in sx]
    dist =  sx - bx[closest]
    for n,c in enumerate(closest):
        if dist[n] < tol:
            new_y.append(by[c])
        else:
            if c == 0:  # near edge case
                intp_x = bx[:interp]
                intp_y = by[:interp]
            elif c == (len(bx)-1):  # farside edge case
                intp_x = bx[-interp+1:]
                intp_y = by[-interp+1:]
            else:  # everthing else...
                intp_x = bx[c-(interp-1)//2 : c-(interp-1)//2+1]
                intp_y = by[c-(interp-1)//2 : c-(interp-1)//2+1]

            A = np.vstack([intp_x, np.ones(len(intp_x))]).T  # interpolates between closest values
            m, c = np.linalg.lstsq(A, intp_y)[0]
            new_y.append((m*sx[n] + c))
    return sx, new_y


def trim(data, model):
    # gets dusty model range that matches data
    indexes =  np.logical_and(model[0]>=data[0][0],model[0]<=data[0][-1])
    return np.vstack([model[0][indexes],model[1][indexes]])


model_names = get_models(directory) 

# plotting stuff
fig, axs = plt.subplots(math.ceil(len(targets)/4),4, sharex=True, sharey=True, figsize=(16,20))
axs = axs.ravel()

for counter,target in enumerate(targets):
    stat_values = []
    data = get_data(target)
    model = trim(data,get_dusty(model_names[0]))
    data = resample(model,data)

    for model_fname  in model_names:
        stat_values.append(fit_norm(data,model_fname))
    stat_array = np.vstack(stat_values)
    argmin = np.argmin(stat_array)
    model_index = argmin // stat_array.shape[1]
    trial_index = argmin % stat_array.shape[1]
    # print(target,model_names[model_index],trials[trial_index])

    # calculated luminosity
    luminosity=np.power(10.0,distance_norm-math.log10(trials[trial_index])*-1)

    # gets output file for mass loss, optical depth, expansion velocity, etc.
    output_files=get_dusty_outputs(directory)
    output_array=np.genfromtxt((str(directory)+'/'+str(directory)+'_outputs/'+str(model_names[model_index].split('.')[:-1][0]).split('/')[-1]+".out"), dtype=[('number',np.float64),('odep',np.float64),('c',np.float64),('d',np.float64),('e',np.float64),('f',np.float64),('g',np.float64),('h',np.float64),('mdot',np.float64),('vexp',np.float64),('i',np.float64)], comments ="*" , delimiter='', skip_header=46, skip_footer=15)
    output_snumber=int(model_names[model_index][-3:])
    output_list=output_array[output_array['number']==output_snumber].squeeze()
    odep=str(output_list['odep'])
    vexp=str(output_list['vexp'])
    # print model_fname
    teff=model_names[model_index].split('.')[-2].split('_')[-2]
    tinner=model_names[model_index].split('.')[-2].split('_')[-1]
    scaled_vexp=float(vexp)*(luminosity/10000)**(0.25)
    mdot=str(output_list['mdot'])
    mdot=str(output_list['mdot'])
    scaled_mdot=output_list['mdot']*((luminosity/10000)**(0.75))*(assumed_rgd/200)**(0.5)

    target_name=(target.split('/')[-1][:15]).replace('IRAS-','IRAS ')
    print(target_name)
    latex_array.append((target_name,str(int(round(luminosity/1000))),str(np.round(scaled_vexp,1)),str(int(teff)),str(int(tinner)), str(odep), "%.3E" % float(scaled_mdot)))


    #printed output
    print()
    print()
    print(('    Target: '+target_name))
    print()
    print()
    print(("Luminosity\t\t"+str(round(luminosity))))
    print(("Optical depth\t\t"+str(odep)))
    print(("Expansion velocity (scaled)\t"+str(round(scaled_vexp,2))))
    print(("Mass loss (scaled)\t\t"+str("%.2E" % float(scaled_mdot))))
    print()
    print()

    #gets data for plotting
    f = lambda dd: np.vstack([dd[0],dd[1]*trials[trial_index]])
    x_model,y_model = f(get_dusty(model_names[model_index]))
    x_data,y_data = get_data(target)
    
    #test
    #gets supplementary spectra
    bonus_spec=[]
    if os.path.exists('./supp_data/'):
        for item in os.listdir('./supp_data/'):
            if fnmatch(item,'IRS*'+target_name.split(' ')[1]+'*'):
                supp_data=np.array(get_supp_data('supp_data/'+item))
                bonus_spec.append(supp_data)

    #plots supplementary spectra
        for i in range(0,len(bonus_spec)):
            supp_plot_array=Table(np.array([[row[0],row[1]] for row in bonus_spec[i]]), names=('wave','lamflam'))
            axs[counter].plot(np.log10(supp_plot_array['wave']),np.log10(supp_plot_array['lamflam']),c='k',linewidth=0.5,zorder=2)

        bonus_phot=[]
        for item in os.listdir('./supp_data/'):
            if fnmatch(item,'phot*'+target_name.split(' ')[1]+'*'):
                supp_data=np.array(get_supp_data('supp_data/'+item))
                bonus_phot.append(supp_data)

    #plots supplementary phot
        for i in range(0,len(bonus_phot)):
            supp_phot_array=Table(np.array([[row[0],row[1]] for row in bonus_phot[i]]), names=('wave','lamflam'))
            axs[counter].scatter(np.log10(supp_phot_array['wave']),np.log10(supp_phot_array['lamflam']),facecolor='white',s=20,edgecolor='k',linewidth=0.5,zorder=1)

        bonus_err=[]
        for item in os.listdir('./supp_data/'):
            if fnmatch(item,'err*'+target_name.split(' ')[1]+'*'):
                supp_data=np.array(get_supp_data('supp_data/'+item))
                bonus_err.append(supp_data)

    #plots supplementary err
        for i in range(0,len(bonus_err)):
            supp_err_array=Table(np.array([[row[0],row[1]] for row in bonus_err[i]]), names=('wave','lamflam'))
            supp_err_array['lamflam'][supp_err_array['lamflam'] == 0] = np.nan
            yerror=np.log10(supp_phot_array['lamflam'])*supp_err_array['lamflam']/supp_phot_array['lamflam']
            axs[counter].errorbar(np.log10(supp_phot_array['wave']),np.log10(supp_phot_array['lamflam']), yerr = yerror,color='0.3', ls='none',linewidth=0.2,zorder=1)

    #logs
    x_model = np.log10(x_model)
    y_model = np.log10(y_model)
    x_data = np.log10(x_data)
    y_data = np.log10(y_data)

    #plots
    axs[counter].set_xlim(0.21,1.79)
    axs[counter].set_ylim(-14.2,-10.51)
    axs[counter].plot(x_model,y_model,c='k',linewidth=0.7, linestyle='--',zorder=2)
    axs[counter].plot(x_data,y_data,c='blue')
    axs[counter].annotate(target_name.replace('-',r'\textendash'),(1.15,-13.75),xycoords='data', fontsize=14)
    axs[counter].get_xaxis().set_tick_params(which='both', direction='in', labelsize=15)
    axs[counter].get_yaxis().set_tick_params(which='both', direction='in', labelsize=15)

plt.subplots_adjust(wspace=0,hspace=0)
fig.text(0.5, 0.085, 'log $\lambda$ ($\mu m$)', ha='center', fontsize=16)
fig.text(0.08, 0.5, "log $\lambda$ F$_{\lambda}$ "+"(W m$^{-2}$)", va='center', rotation='vertical', fontsize=16)

fig.savefig('all_gb_seds.png',dpi=500,bbox_inches='tight')
    

a=Table(np.array(latex_array), names=('source','L', 'vexp_predicted', 'teff', 'tinner', 'odep', 'mdot'), dtype=('S16', 'int32', 'f8', 'int32', 'int32', 'f8', 'f8'))

a['L']=a['L']*1000
a.remove_row(-1)
a.write('gb_latex_table.csv', format='csv', overwrite=True)
pool.close()



















