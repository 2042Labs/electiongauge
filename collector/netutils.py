#!/usr/bin/env python
# encoding: utf-8
"""
netutils.py

Encapsulate all convenience functions written for analysis of hashtag and retweet networks

>>> DEPRECATES retweet_net.py and hashnet.py <<<

Created by Maksim Tsvetovat on 2011-05-10.
Copyright (c) 2011 __MyCompanyName__. All rights reserved.
"""

import networkx as net
import matplotlib.pyplot as plot
import csv
from dateutil.parser import *
import math
import numpy as num
import logging

class NetUtils(object):
    def __init__(self):
        logging.basicConfig()
        self.l = logging.getLogger('NetUtils')
        self.l.setLevel(4) ## set debug level to "every fucking thing"
        
    def add_or_inc_edge(self, g,f,t):
        """
        Adds an edge to the graph IF the edge does not exist already. 
        If it does exist, increment the edge weight.
        Used for quick-and-dirty calculation of projected graphs from 2-mode networks.
        """
        if g.has_edge(f,t):
            g[f][t]['weight']+=1
        else:
            g.add_edge(f,t,weight=1)
        
    def sorted_degree(self, g):
        d=net.degree(g)
        ds = sorted(d.iteritems(), key=lambda (k,v): (-v,k))
        return ds
    
    def sorted_eigen(self, g):
        d=net.eigenvector_centrality(g)
        ds = sorted(d.iteritems(), key=lambda (k,v): (-v,k))
        return ds

    def sorted_pagerank(self, g):
        d=net.pagerank(g)
        ds = sorted(d.iteritems(), key=lambda (k,v): (-v,k))
        return ds


    def trim_edges(self, g, weight=1):
        """
        Remove edges with weights less then a threshold parameter ("weight")
        """
        g2=net.Graph()
        for f, to, edata in g.edges(data=True):
            if edata['weight'] > weight:
                g2.add_edge(f,to,edata)
        return g2

    def edge_weights(self, g):
    	return [2*math.log(edata['weight']) for f,to,edata in g.edges(data=True)]

    def trim_degrees(self, g, degree=1):
        """
        Trim the graph by removing nodes with degree less then value of the degree parameter
        Returns a copy of the graph, so it's non-destructive.
        """
        g2=g.copy()
        d=net.degree(g2)
        for n in g2.nodes():
            if d[n]<=degree: g2.remove_node(n)
        return g2
        

    def qd_pajek_parser(self,filename):
        """
            ### A QUICK AND DIRTY PAJEK PARSER
            Occasionally, NetworkX fails to parse Pajek files that it generates! (bug report submitted to the authors)
            This is a quick and dirty parser that is very liberal in what it accepts. It doesn't FULLY support the .NET format
            but if it doesn't understand something, it really doesn't care (and skips it rather then crashing-and-burning)
            
            Just give it a file name and out comes a graph.
        """
        r=open(filename)
        mode=0
        g=net.Graph()
        nmap={}
        for row in r:
            if row.startswith('*'):
                if mode==0: 
                    mode=1
                elif mode==1: 
                    mode=2
                elif mode==2: 
                    mode=3
                continue

            ## reading the nodes
            if mode==2:
                nd=row.split()
                nmap[nd[0]]=nd[1]
                g.add_node(nd[1])
            elif mode==3:
                eg=row.split()
                f=nmap[eg[0]]
                t=nmap[eg[1]]
                try: 
                    v=float(eg[2])
                except ValueError:
                    v=eg[2]
                except IndexError:
                    v=""
                g.add_edge(f,t,weight=v)
        return g        



    def plot_components(self, g, file_name='component', trim=10,format='png'):
    	i=1
    	for component in net.connected_component_subgraphs(g):
    		if len(component.nodes()) < trim: continue
    		print i
    		plot.clf()
    		fig=plot.gcf()
    		fig.set_size_inches(16,12)
    		fig.set_dpi(240)
    		pos=net.spring_layout(component)
    		d=net.degree_centrality(component)
    		ew=edge_weights(component)  
    		ns=[x*100 for x in d.values()]
    		net.draw_networkx(component, pos=pos, with_labels=True, font_size=4, width=1,node_size=ns,edge_color=ew,edge_cmap=plot.cm.Reds)
    		plot.savefig(file_name+'_'+str(i)+'.'+format)
    		i=i+1


    def plot_egonet(self, g,name,file_name="egonet_", format='pdf'):
        egonet=net.generators.ego.ego_graph(g,name,radius=2)
        print name, len(egonet.nodes())
        plot.clf()
        net.draw(egonet,with_labels=True)
        plot.savefig(file_name+name+"."+format)
        return [len(egonet.nodes()),net.density(egonet)]

    ## g = Graph
    ## nodelist = list(of [node, attrib, attrib, attrib] that we should compute ego metrics for). Default = compute all
    ## header = list of column headings for attributes
    ## file_name = prefix for output files
    ## plot_egonets = False by default; if True, plot top 10 people's ego networks
    ## attrib = list of node attributes to put into the table
    def ego_metrics(self, g, nodelist=None, header=[], filename="", plot_egonets=False):
        if nodelist==None: 
            nodelist=[[n] for n in g.nodes()] 
        tmp={}
        w=csv.writer(open(filename+"ego_metrics.csv",'wb'))
        hdr=['name','egonet size','egonet density','degree','2nd degree']
        hdr.extend(header)
        w.writerow(hdr)
        
        print len(g), len(nodelist)
        
        d=net.degree(g)
        c=d
        b=d
     #   c=net.closeness_centrality(g)
     #   b=net.betweenness_centrality(g)
        for row in nodelist:
            n=row[0]
            if n not in g: continue
            egonet=net.ego_graph(g, n, 2)
            size=len(egonet)
            if size < 2: 
                continue
            density=net.density(egonet)
            #values.append([n,size,density])
            tmp[n[0]]=size
            out=[n,size,density,d[n],(d[n]*147)/(2*math.log10(d[n])+1)]
            out.extend(row[1:])
            w.writerow(out)  

        if plot_egonets:        
            #get a sorted list of ego-net sizes
            w=csv.writer(open(filename+"top_10_metrics.csv",'wb'))
            w.writerow(['name','egonet size','egonet density','degree','closeness','betweenness'])
            ds = sorted(tmp.iteritems(), key=lambda (k,v): (-v,k))
            for key in [k[0] for k in ds[0:10]]:
                [size,density]=self.plot_egonet(g,key,file_name=filename+"_egonet_")
                w.writerow([key,size,density,d[key],c[key],b[key]])

    def ego_metrics_gen(self, g, nodes=None):
        if nodes==None:
            nodes=g.nodes()

        self.l.info("Nodes in Graph:"+str(len(g)) +" Nodes in Nodelist:"+ str(len(nodes)))
        
        d=net.degree(g)
        c=d
        b=d
        for n in nodes:
            if n not in g: continue
            egonet=net.ego_graph(g, n, 2)
            size=len(egonet)
            if size < 2:
                continue
            density=net.density(egonet)
            out=[n,size,density,d[n],(d[n]*147)/(2*math.log10(d[n]+1))]
            yield dict(zip(['name','egonet size','egonet density','degree','closeness'], out))
