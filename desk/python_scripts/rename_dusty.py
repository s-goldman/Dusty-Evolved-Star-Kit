import numpy as np
a=[]

for i in range(2600,3600,200):
	for j in range(600,1300,200):
		a.append('astronomical_'+str(i)+'_'+str(j))


for i in range(0,len(a)):
	filename=str(a[i])+".inp"
	a_teff=(a[i].split('_')[1])
	a_tinner=(a[i].split('_')[2])
	open(filename,'w').write(open("template_astronomical.inp",'r').read().format(Teff=a_teff, Tinner=a_tinner, od1="0.1",od2="50"))

np.savetxt('dusty.inp', a, fmt='%s', delimiter='\n')