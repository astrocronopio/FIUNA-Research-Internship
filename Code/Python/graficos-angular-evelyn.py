
from datetime import datetime

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

import matplotlib as mpl
mpl.rcParams.update({
	'font.size': 16,
	'figure.figsize': [12, 10],
	'figure.autolayout': True,
	'font.family': 'serif',
	'font.serif': ['STIXGeneral']})


path_csv='../../Local-Machine/Datasets/muones/muones.csv'
df=pd.read_csv('../../Local-Machine/Datasets/muones/rangos.csv')
omegas=df["Omega"].tolist()

def main():
    labels=[]
    ticks=[]

    countsplot=[]
    
    countsplots=[[] for j in range(11)]
    
    timesplot=[]

    num = np.arange(14,144 + 13,13)
    print(num)

    times=(pd.read_csv(path_csv))['datetime'].to_list()

    counts=[]
    
    for n in num:
        counts.append((pd.read_csv(path_csv))[str(n )].to_list())


    for k in range(0,len(times)):
        times[k]=(datetime.fromtimestamp(times[k])).strftime("%Y-%m-%d \n %H:%M:%S")

    #Aqui se construye el vector de la suma de los verticales
    for k in range(int(len(times)*10/3600)):
        timesplot.append(times[360*k])
        sum_counts = 0

        for m in range(len(num)):
            countsplots[m].append( sum(counts[m][360*k:360*(k+1)])/(omegas[num[m]-1]))
            sum_counts += countsplots[m][k]

        countsplot.append(sum_counts)

    py=pd.DataFrame({'Cuentas':countsplot},index=timesplot)
    flagPy1=np.logical_and(py.index>"2021-04-04",py.index<"2021-04-15")

    for k in range(0,len(py.index)):
        if (int(py.index[k].split(' \n ')[1].split(':')[0])%6==0):
            labels.append(py.index[k])
            ticks.append(k)


    plt.figure(figsize=(int(1.25*len(labels)),10))
    py['Cuentas'][flagPy1].plot(marker='.',markersize=7, linestyle='None',legend=True,alpha=1,color='b', subplots=True)
    ax=plt.gca()

    #ax.plot(n_aux,D*ajust+C)

    plt.ylim(0,3*max(countsplot)/2)
    plt.xticks(ticks,labels,rotation='vertical')
    ax.set_ylabel('Total de muones')

    ax.set_title('Suma total de muones de incidencia vertical')
    plt.grid()
    plt.show()

    
    pass

if __name__ == '__main__':
    main()
    