#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
# $1 - column: UTC time, interval 10 seconds

##### Columns of total muons data #######

# $15,  $28,  $41,  $54,  $67,  $80,  $93,  $106, $119, $132,   $145
# A1B1, A2B2, A3B3, A4B4, A5B5, A6B6, A7B7, A8B8, A9B9, A10B10, A11B11 

#It makes sense after seeing  detector.jpeg 

#### Special columns #####

#$22     $20     #70     #68      #105     #77     $127      $125
#A1B8   #A1B6   #A5B8   #A5B6    $A8B7    $A6B3   $A10B5    $A10B3

$1 , sum_total, sum_special, sum_total, $22, $20, $70, $68, $105, $77, $127,  $125 , ___phi____
0	  1				2			3			4	 5	  6    7  	8	 9		10	 11			12


Phi puede tener el valor -9999 que es como que no se midió, para eso se puede reemplazar por la media
entre los dos últimos valores medidos


Storms:

[13:36, 6/4/2021] Jorge Molina: 1) 12/05 (00:00  - 19:00)    1620792000  - 1620860400
[13:36, 6/4/2021] Jorge Molina: 2) 19/05 15:00 - 21/05 8:00  1621465200  - 1621598400
[13:37, 6/4/2021] Jorge Molina: 3) 26/05 00:00 - 28/05 00:00 1622001600  - 1622174400
"""

import matplotlib.pyplot as plt
import numpy as np
import matplotlib.dates as mdates
import datetime as dt
import matplotlib as mpl

mpl.rcParams.update({
	'font.size': 16,
	'figure.figsize': [12, 6],
	'figure.autolayout': True,
	'font.family': 'serif',
	'font.serif': ['STIXGeneral']})

muon_rtsw_data="../../../Local-Machine/Datasets/muons_rtsw_merged_data_1h_bin.txt"
# muon_rtsw_data="../../../Local-Machine/Datasets/muons_rtsw_merged_data_30-min_bin.txt"

TOWARDS_AWAY_LIMIT = 225

utc_i_storm1, utc_f_storm1 = 1620792000 , 1620860400
utc_i_storm2, utc_f_storm2 = 1621465200 , 1621598400
utc_i_storm3, utc_f_storm3 = 1622001600 , 1622174400


def main():

	utc, total, phi =  np.loadtxt(muon_rtsw_data, usecols=(0,3,12), unpack=True)
	dateconv = np.vectorize(dt.datetime.fromtimestamp)
	date = dateconv(utc)
 
	mean_total = np.mean(total)
	std_dev	= np.std(total)

	flag = np.sign(phi-TOWARDS_AWAY_LIMIT)
	towards=[[],[]]
	away=[[],[]]
	towards_storms=[[],[]]
	away_storms=[[],[]]
	
	for i in range(len(total)):
		if flag[i]==1:
		
			towards[0].append(date[i])
			towards[1].append(total[i])
			
			if utc[i] >= utc_i_storm1 and utc[i] <= utc_f_storm1:
				towards_storms[0].append(date[i])
				towards_storms[1].append(total[i])
		
			elif utc[i] >= utc_i_storm2 and utc[i] <= utc_f_storm2:
				towards_storms[0].append(date[i])
				towards_storms[1].append(total[i])
		
			elif utc[i] >= utc_i_storm3 and utc[i] <= utc_f_storm3:
				towards_storms[0].append(date[i])
				towards_storms[1].append(total[i])
		
		elif flag[i]==-1:
		
			away[0].append(date[i])
			away[1].append(total[i])

			if utc[i] >= utc_i_storm1 and utc[i] <= utc_f_storm1:
				away_storms[0].append(date[i])
				away_storms[1].append(total[i])

			elif utc[i] >= utc_i_storm2 and utc[i] <= utc_f_storm2:
				away_storms[0].append(date[i])
				away_storms[1].append(total[i])

			elif utc[i] >= utc_i_storm3 and utc[i] <= utc_f_storm3:
				away_storms[0].append(date[i])
				away_storms[1].append(total[i])
		
		else:
			print("error")

	towards = np.array(towards)
	away = np.array(away)
 
	towards_storms = np.array(towards_storms)
	away_storms = np.array(away_storms)




	fig, ax1 = plt.subplots()
 
	##Plotting##
	ax1.plot(towards[0],(towards[1] - mean_total)/std_dev, 
          linewidth=0.5, label="Towards", color="indianred", 
          alpha=0.3, marker='o', markersize=5)
 
	ax1.plot(away[0],(away[1] - mean_total)/std_dev, 
          linewidth=0.5, label="Away", color='darkblue', 
          alpha=0.3, marker="s", ms=4)
 
	ax1.plot(towards_storms[0],(towards_storms[1] - mean_total)/std_dev, 
          linewidth=0.5, label="Towards (Storms)", color="red", 
          alpha=0.75, marker='o', markersize=5)

	ax1.plot(away_storms[0],(away_storms[1] - mean_total)/std_dev, 
          linewidth=0.5, label="Away (Storms)", color="blue", 
          alpha=0.75, marker='o', markersize=5)
	
	# plt.axhline(y=np.mean(total), linestyle=":", color='black', linewidth=1.2, label="Media Total ")
	# ax1.axhline(y=(np.mean(towards[1]) - mean_total)/std_dev, 
    #          linestyle="-.", color='indianred', linewidth=1.2, label="Media Total ")
	
 	# ax1.axhline(y=(np.mean(away[1]) - mean_total)/std_dev, 
    #          linestyle=":", color='darkblue', linewidth=1.2, label="Media Total ")
	
 	# plt.scatter(date, total, label="Total", alpha=0.2)
	
	ax1.set_ylabel("Muon Count sigmas")
	ax1.legend(ncol=2)
	ax1.set_title("Muon Mean: {:.3f}, Muon sigma: {:3f}".format(mean_total, std_dev))


	ax2 = ax1.twinx()
	ax2.plot(date, phi, color='grey', alpha=0.3)
	ax2.set_ylabel("Phi", color='grey')

	ax=plt.gca()
	xfmt = mdates.DateFormatter(fmt='%m/%d')
	# ax.xaxis.set_major_locator(mdates.YearLocator())
	ax.xaxis.set_minor_locator(mdates.DayLocator())
	ax.xaxis.set_minor_locator(mdates.MonthLocator())
	ax.xaxis.set_major_formatter(xfmt)
	plt.show()
	pass

if __name__ == '__main__':
    	main()
	
