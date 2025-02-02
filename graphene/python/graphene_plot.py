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

# matplotlib.use('Qt5Agg')
# import seaborn as sns

plt.rcParams.update({'font.size': 18,
					 'lines.linewidth': 2,
					 'font.family':'sans-serif'})
plt.figure(figsize=(8.5,6))

def moving_average(x,w):
	# ret = np.cumsum(x, dtype=float)
	# ret[w:] = ret[w:] - ret[:-w]
	# return ret[w-1:]/w
	return np.convolve(x, np.ones(w), 'valid')/ w


paths = ['ISO-Full/Graphene_REBO_Strain.SA-ISO-*.txt',  
		 'NVT-Full/Graphene_REBO_Strain.SA-NVT-*.txt',
		 'NPT-Full/Graphene_REBO_Strain-*-1000.txt'
		 # 'NPT-Full/Graphene_REBO_Strain-*-1000.txt',
		 # 'NPT-Full/Graphene_REBO_Strain-*-10000.txt',
		 # 'NPT-Full/Graphene_REBO_Strain-*-100000.txt',
		 # 'NPT-Full/Graphene_REBO_Strain-*-1000000.txt',
		 # 'NPT-Full/Graphene_REBO_Strain-*-10000000.txt',
		 # 'NPT-Full/Graphene_REBO_Strain-*-100000000.txt',
		 # 'NPT-Full/Graphene_REBO_Strain-*-1000000000.txt'
		 ]

for _i, filepath in enumerate(paths):

	txt = glob.glob(filepath)

	file = []
	for textfile in txt:
		file.append(textfile)

	runlen = len(file)

	Dist_Dict = {}
	Int_Dict = {}

	maxy = []
	maxstrain = []

	for i in range(0,runlen):
		#${temps} ${strainy} ${strainx} ${SA_stressxx} ${SA_stressyy} ${SA_stressxy}
		data = pd.read_csv(file[i], skiprows=1, delimiter=' ', names=['Temp','strain', 'strainx', 'xx', 'yy', 'xy'])

		key = 'Dist'+str(i)
		val = 'Int'+str(i)

		strain = data.strain
		xx = data.xx
		yy = data.yy
		xy = data.xy

		xx = np.array(xx)
		yy = np.array(yy)
		xy = np.array(xy)
		strain = np.array(strain)

		xx = xx - xx[0]
		yy = yy - yy[0]
		xy = xy - xy[0]
		strain = strain - strain[0]

		xx = moving_average(xx, 50)
		yy = moving_average(yy, 50)
		xy = moving_average(xy, 50)
		strain = moving_average(strain, 50)

		# Dist_Dict[key] = np.array(zz)
		# # Int_Dict[val] = np.array(ke)+np.array(pe) # 
		# Int_Dict[val] = np.array(couple)

		# find first peak only

		_found = False
		my = 1

		for _l, _y in enumerate(yy):
			if not _found and _y > my:
				my = _y
				ind = _l
			elif my > 100:
				_found = True

		maxy.append(my)
		# ind = np.where(yy==my)[0][0]
		maxstrain.append(strain[ind])

		# if _i == 0:
		# 	plt.plot(strain, yy/10**9, 'b', alpha=0.1)
		# 	plt.plot(strain[ind], my/10**9, 'bo')
		# elif _i == 1:
		# 	plt.plot(strain, yy/10**9, 'r', alpha=0.1)
		# 	plt.plot(strain[ind], my/10**9, 'ro')
		# else:
		# 	plt.plot(strain, yy/10**9, 'g', alpha=0.1)
		# 	plt.plot(strain[ind], my/10**9, 'go')


	maxy = np.array(maxy)/10**9


	avgy = np.mean(maxy)
	stdy = np.std(maxy)
	avgstrain = np.mean(maxstrain)

	
	colors = ['r', 'g', 'b']

	plt.hist(maxy, bins=20, density=True, alpha=0.2, color=slicedCM[_i])
	xmin, xmax = plt.xlim()
	
	x = np.linspace(xmin, xmax, len(maxstrain))

	ae, loce, scalee = skewnorm.fit(maxy)
	plt.plot(x,skewnorm.pdf(x,ae, loce, scalee), linewidth = 3, color=slicedCM[_i])




xmin, xmax = plt.xlim()
plt.xlim([np.floor(xmin), np.ceil(xmax)])
plt.ylim([0, 1])

plt.xlabel('Ultimate Stress [GPa]')
plt.ylabel('Probability')

plt.show()	
