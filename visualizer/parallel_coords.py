#!/usr/bin/python
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import json as json
import random
from collections import defaultdict

    
def plot_parallel(keys, gauges,name="gauges"): 
    plt.clf()
    data=defaultdict(list)
    for k in sorted(keys):
        for can in gauges[k]:
            data[can].append(gauges[k][can])
    
    colors=['r','g','b','c','m','k','y'][:len(data.keys())]

    i=0
    for can in sorted(data.keys()):
        plt.plot(range(len(keys)), data[can], colors[i],label=can)
        plt.xticks(range(len(keys)), keys, size='small')
        i+=1

    plt.legend()
    plt.savefig('../egauge/static_assets/data/'+name+'.png')


def main():  
    plt.ioff()
    dataPath="../egauge/static_assets/data/"
    jsonPath=dataPath+"json/"    

    gauges=json.loads(open(jsonPath+'gauges.json','rb').read())

    #keys=gauges.keys()[:10]
    feb='AZ MI WA'.split(' ') 
    superTuesday='AK GA ID MA ND OH OK TN VT VA'.split(' ')

    plot_parallel(feb,gauges,name='feb')
    plot_parallel(superTuesday,gauges,name='superTuesday')
    


if __name__ == '__main__':
    main()
    





