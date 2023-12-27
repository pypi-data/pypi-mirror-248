import inspect
def func():

    '''
	import pandas as pd
	import numpy as np
	filename=pd.read_csv('Weather.csv',header=None)
	concepts=np.array(filename.iloc[:,0:-1])
	target=np.array(filename.iloc[:,-1])
	print(concepts)
	print(target)
	def learn(concepts,target):
    		print("initialisation:")
    		spe_h=concepts[0].copy()
    		gen_h=[['?' for i in range(len(spe_h))] for i in range(len(spe_h))]
    		print(spe_h)
    		print(gen_h)
    		for i,h in enumerate(concepts):
        		if target[i]=='Yes':
            			for x in range(len(spe_h)):
                			if(h[x]!=spe_h[x]):
                    				spe_h[x]='?'
                    				gen_h[x][x]='?'
        		if target[i]=='No':
            			for x in range(len(spe_h)):
                			if(h[x]!=spe_h[x]):
                    				gen_h[x][x]=spe_h[x]
                			else:
                    				gen_h[x][x]='?'
       		        print("hypothesis ",i+1)
        		print(gen_h)
        		print(spe_h)
    	indices=[i for i,val in enumerate(gen_h) if val== ['?','?','?','?','?','?']]
    	for i in indices:
        	gen_h.remove(['?','?','?','?','?','?'])
        return spe_h, gen_h
	final_spe,final_gen=learn(concepts,target)
	print("specific:",final_spe)
	print("general",final_gen)
   
   '''
   
def px():
    code=inspect.getsource(func)
    print(code)

