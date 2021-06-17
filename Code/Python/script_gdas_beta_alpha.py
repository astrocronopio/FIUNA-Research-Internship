# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %%
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

import pandas as pd
import pytz, datetime
import pytz
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from scipy import stats
from sklearn.linear_model import LinearRegression 
from sklearn import metrics

import matplotlib as mpl
from matplotlib import gridspec
mpl.rcParams.update({
	'font.size': 16,
	'figure.figsize': [10, 8],
	'figure.autolayout': True,
	'font.family': 'serif',
	'font.serif': ['STIXGeneral']})



MOVING_AVERAGE_WINDOW_MUON = 12
MOVING_AVERAGE_WINDOW_GDAS = 12


"""GDAS dataset"""
gdas = pd.read_csv('teffDatatotal2021.csv',delimiter=",", skiprows=1, names=['id','date','teff', 'ts', 'ps'],lineterminator='\n')
gdas .drop(columns=['id'])
gdas['date']=pd.to_datetime(gdas.date, format='%Y-%m-%d %H:%M:%S',utc=True)
gdas.set_index(['date'],drop=True, inplace=True)

# According to Auger; density = 0.3484P / T + 273.16 ,
density = 0.3484 * gdas['ps']/gdas['teff']
gdas['den'] = density

"""Muon dataset"""
py = pd.read_csv('total_de_muones.csv')
py['datetime']=pd.to_datetime(py.Time,format='%Y-%m-%d %H:%M:%S',utc=True)
py.set_index(['datetime'],drop=True, inplace=True)
py=py.resample('H').sum()


"""Misc."""
flagPy=np.logical_and(py.index>="2021-04-23",py.index<="2021-05-31")
py=py[flagPy]

"""¿Qué ese ese valor 150 000 y porque ese un límite?"""

flag=py['sumaTodos'].values>150000
py=py[flag]
sup=np.max(py['sumaTodos'].values) #Para el rango            
inf=np.min(py['sumaTodos'].values) #Para el rango  
py.tail()


def plot_moving_average_muons():
    fig, axes = plt.subplots(1,1, figsize=(15,5), sharex=True)

    #PLOTTING MUONS COUNTS
    axes.set_title("Total muons count and moving average")
    py['sumaTodos'].plot(subplots=True, 
                         ylim=(inf,sup), 
                         linestyle='-', ax=axes, alpha=0.6, 
                         color='red', label="Total Muons")
    
    """Plot Moving average Muons"""
    py['sumaTodos_med']=py['sumaTodos'].rolling(MOVING_AVERAGE_WINDOW_MUON,center=True).median()
    
    py['sumaTodos_med'].plot(subplots=True,     marker='.',
                             ylim=(inf,sup),    markersize=1, 
                             color='black',     linestyle=':', 
                             ax=axes, alpha=0.8, linewidth=2,
                             label="Moving average: {}".format(MOVING_AVERAGE_WINDOW_MUON))

    axes.set_ylabel('Counts')
    axes.set_xlabel('Date')
    axes.legend()
    plt.tight_layout()

def plot_moving_average_GDAS():

    fig, axes = plt.subplots(3,1, figsize=(15,10), sharex=True)
    
    #Pressure
    gdas['ps'].plot(subplots=True,marker='s', markersize=3, 
                    linestyle='None', ax=axes[0], 
                    label="Pressure [hPa]")
    """Moving average GDAS"""
    gdas['ps_med']=gdas['ps'].rolling(MOVING_AVERAGE_WINDOW_GDAS,center=True).median()
    gdas['ps_med'].plot(subplots=True,marker='.',markersize=1, 
                        color='red',linestyle='-', ax=axes[0],
                        label="Average Pressure: {}".format(MOVING_AVERAGE_WINDOW_GDAS ))

    axes[0].set_ylabel('Pressure [hPa]')
    axes[0].set_xlabel('Date')
    axes[0].legend()

    # Effective Temperature
    gdas['teff'].plot(subplots=True,marker='.', markersize=4, 
                      linestyle='None', ax=axes[1])
    axes[1].set_ylabel('Temperature [K]')
    axes[1].set_xlabel('Date')
    
    #Density
    gdas['den'].plot(subplots=True,marker='.', markersize=4, 
                     linestyle='None', ax=axes[2])
    axes[2].set_ylabel("Density $\\rho$ [g/cm$^3$]")
    axes[2].set_xlabel('Date')

    plt.tight_layout()

def dIoIm_combined_dataset(plot_flag=True):    
    
    countsClean =   py
    combined    =   gdas.join(countsClean['sumaTodos'], how='outer')
    combined    =   combined.drop(combined.index[0])

    flag1 = np.logical_and(combined.index>="2021-04-23",combined.index<="2021-05-31")

    #Counts per half an hour
    Im = combined['sumaTodos'].dropna().mean()


    """############## MAIN LINEs OF CODE ##############"""

    # delta count 
    combined['dIoIm']=(combined['sumaTodos'][flag1]-Im)/(Im)*100
    combined['lndIoIm']= np.log(combined['dIoIm']/100)

    #delta pressure
    P0=combined['ps'][flag1].dropna().mean()
    combined['dP']=(combined['ps'][flag1]-P0)

    #delta temperature
    Tg=combined['teff'][flag1].dropna().mean()
    combined['dTg']=(combined['teff'][flag1]-Tg)
    
    #delta density
    Deng=combined['den'][flag1].dropna().mean()    
    combined['dDen']= (combined['den'][flag1]-Deng)

    #Plot all  variables
    var = ['lndIoIm', 'dIoIm', 'dP', 'dDen']
    # var_latex = ["$log (\Delta I / I_{mean})$", "100*$\Delta I / I_{mean}$", "$\Delta P$", "$\Delta \\rho$" ]
    if plot_flag:
        axes = combined[var][flag1].plot(marker='o', markersize=2 ,
                                        linestyle='None', figsize=(11, 9), 
                                        subplots=True, alpha=0.7, label=None)
        for ax,v in zip(axes,var):
            ax.set_ylabel(v)
    
    """############## END LINEs OF CODE ##############"""
    
    """ Combine dataset in given range of time and uncertainty"""

    combined=combined[flag1]

    var='dIoIm'
    max_dist = np.percentile(combined[var][~np.isnan(combined[var])], 75)
    min_dist = np.percentile(combined[var][~np.isnan(combined[var])], 25)
    distance = 1.5 * ( max_dist - min_dist )
    
    fA  = combined[var]< distance + max_dist
    fB  = combined[var] > min_dist - distance
    
    fC  = np.isnan(combined[var]) 
    
    combinedNew=combined[np.logical_or(np.logical_and(fA,fB),fC)]

    flagNa=~np.isnan(combinedNew[var].values)

    #Interpolate GDAS data#
    ##Importante: como interpola la funcion interpolate?
    
    combinedNew = combinedNew.apply(pd.Series.interpolate, args=('index',) )
    
    ## Final dataset, full non-nan values, in desired range.
    combinedNew=combinedNew[flagNa]

    return combinedNew 

def beta_fit(combinedNew, plot_flag=True):

    combinedNewHour=combinedNew.resample('H').mean()
    combinedNewHour['dIoIm']
    combinedNewHour=combinedNewHour.dropna()

    if plot_flag:
        
        var = ['dIoIm', 'dP','dTg', 'dDen']
        axes = combinedNewHour[var].plot(marker='.',markersize=5, linestyle='None', alpha=0.6, figsize=(11, 9), subplots=True)
        for ax,v in zip(axes,var):
            ax.set_ylabel(v)
        plt.figure(20)
        

    print("\n\n## REGRESSION beta: dP vs dIoIm ##")
    print("\nFitting Results: y = ax + b")
    lm = LinearRegression() 
    X = combinedNewHour['dP'].values.reshape(-1,1) #makes it 1D
    Y = combinedNewHour['dIoIm'] 
    
    lm.fit(X,Y)
    pred=lm.predict(X)
        
    print("b: " , lm.intercept_)
    print("a: " , lm.coef_[0])
    print("\nR-squared value of this fit:",round(metrics.r2_score(Y,pred),3))

    #Print correlation#    
    print("Correlation: ", combinedNewHour['dP'].corr(combinedNewHour['dIoIm']), "\n\n")
    
    #plot fit
    plt.figure(27)
    plt.title("Pressure")
    sns.regplot('dP', 'dIoIm', combinedNewHour)
    
    #Correcting datafile with new parameters
    combinedNewHour['dIoImPC'] = combinedNewHour['dIoIm']-lm.coef_*combinedNewHour['dP']
    
    return combinedNewHour
    ##############################################

def alpha_fit(combinedNewHour):
    print("\n\n## REGRESSION alfa: dT vs dIoIm ##")
        
    print("\nFitting Results: y = ax + b")
    lmT = LinearRegression() 
    XT=combinedNewHour['dTg'].values.reshape(-1,1)
    YT=combinedNewHour['dIoIm']
    
    lmT.fit(XT,YT)
    predT=lmT.predict(XT)
    
    print("b: ", lmT.intercept_)
    print("a: ", lmT.coef_)
    
    print("\nR-squared value of this fit:",round(metrics.r2_score(YT,predT),3))
    #Print correlation#    
    print("Correlation: ", combinedNewHour['dTg'].corr(combinedNewHour['dIoIm']), "\n\n")
    
    #Plot
    plt.figure(28) 
    plt.title("Temperature")
    sns.regplot('dTg','dIoIm', combinedNewHour)
    
    return

def alpha_fit_density(combinedNewHour):
    print("\n\n## REGRESSION alfa: dDen vs dIoIm (DENSITY) ##")
    print("\nFitting Results: y = ax + b")
    
    lmT = LinearRegression() 
    XT=combinedNewHour['dDen'].values.reshape(-1,1)
    YT=combinedNewHour['dIoIm']
    
    lmT.fit(XT,YT)
    predT=lmT.predict(XT)
    
    print("b: ", lmT.intercept_)
    print("a: ", lmT.coef_)
    
    print("\nR-squared value of this fit:",round(metrics.r2_score(YT,predT),3))
    #Print correlation#    
    print("Correlation: ", combinedNewHour['dDen'].corr(combinedNewHour['dIoIm']), "\n\n")
    
    #Plot
    plt.figure(38) 
    plt.title("Density")
    sns.regplot('dDen','dIoIm', combinedNewHour)
    
    return

def alpha_pressure_corrected_fit(combinedNewHour):
    print("\n\n## REGRESSION alfa: dT vs dIoIm(P correction) ##")

    """
    # Estas líneas me paracen innecesarias, cuando corregis en la línea 
    # anterior, ya sacas la componente de la recta. Te tiene que dar 
    # sí o sí un ajuste horizontal
    
    plt.figure(30)
    #Refitting corrected data.
    sns.regplot('dP','dIoImPC', combinedNewHour)
    
    #Y esto te tiene que dar algo cercano a cero.  Orden e-17 me da.   
    print("Correlation after correction: ", combinedNewHour['dP'].corr(combinedNewHour['dIoImPC']))
    
    """
        
    print("\nFitting Results: y = ax + b")
    lmT = LinearRegression() 
    XT=combinedNewHour['dTg'].values.reshape(-1,1)
    YT=combinedNewHour['dIoImPC']
    
    lmT.fit(XT,YT)
    predT=lmT.predict(XT)
    
    print("b: ", lmT.intercept_)
    print("a: ", lmT.coef_)
    
    print("\nR-squared value of this fit:",round(metrics.r2_score(YT,predT),3))
    #Print correlation#    
    print("Correlation: ", combinedNewHour['dTg'].corr(combinedNewHour['dIoImPC']), "\n\n")
    
    #Plot
    plt.figure(29) 
    plt.title("Temperature (Corrected)")
    sns.regplot('dTg','dIoImPC', combinedNewHour)
    
    #Correction to dataset
    combinedNewHour['dIoImPTC'] =  combinedNewHour['dIoImPC']-lmT.coef_*combinedNewHour['dTg']


    return

    
    
    # %%
    var = ['dIoIm', 'dP','dTg','dIoImPC','dIoImPTC']
    axes = combinedNewHour[var].plot(marker='.',markersize=2.5, linestyle='None', alpha=0.9, figsize=(11, 9), subplots=True)
    #axes = combined[var].plot(marker='.', alpha=1, linestyle='None', figsize=(11, 9), subplots=True)
    for ax,v in zip(axes,var):
        ax.set_ylabel(v)


    combinedNewHour.head()
    combinedNewHour.tail()


    combinedNewHour['Year'] =combinedNewHour.index.year
    combinedNewHour['Month'] = combinedNewHour.index.month
    combinedNewHour['day'] = combinedNewHour.index.day
    combinedNewHour['hour'] = combinedNewHour.index.hour
    combinedNewHour['hour3'] = combinedNewHour.index.hour-3


    # %%
    ax = plt.gca()
    combinedNewHour['dIoImPTC'].plot(marker='.',markersize=8,ylim=(-10,10), linestyle='dashed',legend=True,label='Muons',alpha=1, figsize=(11, 5),ax=ax)
    ax_secondary =combinedNewHour['dP'].plot(ax=ax,marker='.',markersize=8, label='Pressure', linestyle='dotted',
        legend=True, secondary_y=True, color='r')
    ax.set_ylabel('dIoImPTC')


    # %%
    ax = plt.gca()
    combinedNewHour['dIoImPTC'].plot(marker='.',markersize=8,ylim=(-10,10), linestyle='dashed',legend=True,label='Muons(porcentual)',alpha=1, figsize=(11, 5),ax=ax)
    ax_secondary =combinedNewHour['dIoIm'].plot(ax=ax,marker='.',markersize=8, label='Muons', linestyle='dotted',
        legend=True, secondary_y=True, color='r')
    ax.set_ylabel('dIoImPTC')

def alpha_beta_fit(combinedNewHour):
    print("\n\n## REGRESSION alfa y beta: (dT y dP) vs dIoIm (DENSITY) ##")
    print("\nFitting Results: y = a1*T + a2*P + b")
    
    lmT = LinearRegression() 
    XT= pd.DataFrame(combinedNewHour, columns=['dTg','dP'])
    YT= combinedNewHour['dIoIm']
    
    lmT.fit(XT,YT)
    
    print("b: ", lmT.intercept_)
    print("a1-(alpha): ", lmT.coef_[0])
    print("a2-(beta): ", lmT.coef_[1])
    
    print("\nR-squared value of this fit:", lmT.score(XT,YT))
    #Print correlation#    
    print("Correlation: ", combinedNewHour['dDen'].corr(combinedNewHour['dIoIm']), "\n\n")
    
    #Plot
    plt.figure(48) 
    
    sns.regplot('dP', 'dIoIm', combinedNewHour)
    sns.regplot('dTg', 'dIoIm', combinedNewHour)
    
    return    

def main():
    # plot_moving_average_muons()
    # plot_moving_average_GDAS()
    
    data = dIoIm_combined_dataset(False)
    # data = beta_fit(data, False)
    # alpha_fit(data)
    # alpha_fit_density(data)
    
    # alpha_pressure_corrected_fit(data)
    
    alpha_beta_fit(data)
    
    plt.show()
    exit(0)

if __name__ == '__main__':
    main()
