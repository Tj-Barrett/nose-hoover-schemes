import os
import glob
import numpy as np
from scipy.stats import linregress, skewnorm, norm
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('TkAgg')

cmap = plt.get_cmap("plasma")
slicedCM = cmap(np.linspace(0, 1, 4))

plt.rcParams.update({'font.size': 20,
                     'lines.linewidth': 3,
                     'font.family':  'sans-serif'})

# matplotlib.use('Qt5Agg')
# import seaborn as sns

def moving_average(x,w):
	# ret = np.cumsum(x, dtype=float)
	# ret[w:] = ret[w:] - ret[:-w]
	# return ret[w-1:]/w
	return np.convolve(x, np.ones(w), 'valid')/ w

txt = []

for i in range(1,21):
	txt.append(f'NPT-Full/Graphene_REBO_Strain-{i}-1000.txt')

for i in range(1,21):
	txt.append(f'NVT-Full/Graphene_REBO_Strain.SA-NVT-{i}.txt')

file = txt

# file = []
# for textfile in txt:
# 	file.append(textfile)

Dist_Dict_xx = {}
Dist_Dict_yy = {}
Dist_Dict_zz = {}

Int_Dict_xx = {}
Int_Dict_yy = {}
Int_Dict_zz = {}
Int_Dict_hydro = {}
Int_Dict_Temp = {}

runlen = len(file)

for i in range(0,runlen):
	data = pd.read_csv(file[i], skiprows=1, delimiter=' ',  names=['Temp','Strainy', 'Strainx', 'StressXX', 'StressYY', 'StressXY'])

	key = 'Dist'+str(i)
	val = 'Int'+str(i)

	xmax = np.max(data.Strainy)

	temp  = data.Temp
	strain = data.Strainy
	xx = data.StressXX
	yy = data.StressYY
	xy = data.StressXY

	# from rate
	# rate = 0.05
	# tms  = 0.001
	# dump_int = 1000
	# adj_rate = rate*tms*dump_int*np.linspace(0,1,len(temp))

	nn = 1

	xx = moving_average(xx,nn)
	yy = moving_average(yy,nn)

	strain = moving_average(strain,nn)

	temp = moving_average(temp,nn)

	
	xx = xx - xx[0]
	yy = yy - yy[0]

	print('\n\n####')
	print(str(file[i]))
	print('####')

	# Smoothed
	Dist_Dict_xx[key] = np.array(strain)

	Int_Dict_xx[val] = np.array(xx)
	Int_Dict_yy[val] = np.array(yy)

	Int_Dict_Temp[val] = np.array(temp)

fig, ax = plt.subplots(figsize=(10,7))


for i in range(0,runlen):
	key = 'Dist'+str(i)
	val = 'Int'+str(i)


	if i<20:
		if i == 0:
			a, = ax.plot(-Dist_Dict_xx[key], Int_Dict_xx[val]/10**9, linestyle='none',alpha = 1, marker='o', markersize=14, markerfacecolor='none', markevery=1000, c=slicedCM[0])
		ax.plot(Dist_Dict_xx[key], Int_Dict_xx[val]/10**9, linestyle='-',alpha = 0.4, marker='o', markersize=14, markerfacecolor='none', markevery=1000, c=slicedCM[0])
		# ax[1].semilogy(Dist_Dict_xx[key], Int_Dict_Temp[val], linestyle='-',alpha = 0.4,  c=slicedCM[0])
	else:
		if i == 20:
			b, = ax.plot(-Dist_Dict_xx[key], Int_Dict_xx[val]/10**9, linestyle='none', alpha = 1, marker='s', markersize=14, markerfacecolor='none', markevery=1000, c=slicedCM[2])
		ax.plot(Dist_Dict_xx[key], Int_Dict_xx[val]/10**9, marker='s', markersize=14, markerfacecolor='none', markevery=1000, linestyle='-',alpha = 0.4, c=slicedCM[2])
		# ax[1].semilogy(Dist_Dict_xx[key], Int_Dict_Temp[val], linestyle='-',alpha = 0.4,  c=slicedCM[2])
# ax[0].legend([r'$\tau_b$=1E2',r'$\tau_b$=1E3',r'$\tau_b$=1E4',r'$\tau_b$=1E5',r'$\tau_b$=1E6',r'$\tau_b$=1E7',r'NVT'], loc='upper right', framealpha=1.0)

# for i in range(0,runlen):
# 	key = 'Dist'+str(i)
# 	val = 'Int'+str(i)

# 	ax[0].plot(Dist_Dict_xx[key], Int_Dict_yy[val]/10**9, linestyle='-',alpha = 0.2, c=slicedCM[i])
	# ax[0].plot(Dist_Dict_xx[key], Int_Dict_zz[val]/10**9, linestyle='-.',alpha = 0.2, c=slicedCM[i])

ax.set_xlim(0,0.12)
ax.set_ylim(-5,20.0)
ax.set_ylabel('Stress [GPa]')

# ax[1].set_ylim(290,10000000)
# ax[1].set_xlim(0,0.12)
ax.set_xlabel('Strain')
# ax[1].set_ylabel('Temp [K]')
# ax[1].set_yticks([10**3, 10**5, 10**7])

ax.legend([a, b],[r'NPT',r'NVT'], loc='upper left', framealpha=1.0)


plt.show()
