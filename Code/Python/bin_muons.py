"""Con este script contamos la cantidad de eventos en un ancho de tiempo definido"""
import numpy as np
import sys

def bin_archive_data(file_muons, file_events, 
                     binWidth, separationWidth=10): #separationWidth= segundos entre dato y dato
	muones = np.loadtxt(file_muons, dtype= int ,delimiter=",")

	data_length = muones.shape[0]
	init_utc=int(muones[0][0])

	nbin=int((int(muones[-1][0]) - init_utc)/binWidth)+2

	binlist=np.zeros(shape=(nbin,muones.shape[1]))

 
	for i in range(data_length):
		j = int(np.floor((separationWidth*i)/binWidth))
		binlist[j][1:-1] += muones[i][1:-1] 	
	
	for j in range(nbin):
		binlist[j][0] = init_utc + binWidth*j-binWidth/2


	np.savetxt(file_events, binlist, fmt="%i", delimiter="," )

def main():
	file_muons 	= "../../../Local-Machine/Datasets/Muons/muons_deleted_spaces.txt"
	file_output	= "../../../Local-Machine/Datasets/Muons/muones_1h_bin.txt"
	
	""" binWidth en segundos"""

	binWidth 	= 3600

	bin_archive_data(file_muons,file_output, binWidth)
	print("Done with {}!\n".format(file_output))
  
if __name__== "__main__":
	main()