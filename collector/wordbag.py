#!/usr/bin/env python
# encoding: utf-8
"""
wordbag.py

Created by Maksim Tsvetovat on 2011-12-08.
Copyright (c) 2011 __MyCompanyName__. All rights reserved.
"""

import sys
import os
import networkx as net

class wordbag(object):

    def __init__(self):
        self.word_graph=net.DiGraph()
        self.counter=0

    def add_or_inc_edge(self,f,t):
        """
        Adds an edge to the graph IF the edge does not exist already. 
        If it does exist, increment the edge weight.
        Used for quick-and-dirty calculation of projected graphs from 2-mode networks.
        """
        g=self.word_graph
        if g.has_edge(f,t):
            g[f][t]['weight']+=1
        else:
            g.add_edge(f,t,weight=1)
 
    def trim_edges(self, g, weight=1):
        """
        Remove edges with weights less then a threshold parameter ("weight")
        """
        g2=net.Graph()
        for f, to, edata in g.edges(data=True):
            if edata['weight'] > weight:
                g2.add_edge(f,to,edata)
        return g2       

    def add_tokens(self,key, tokens):
        if self.counter>1000:
            self.prune()
            self.save()
            self.counter=0
            
        for token in tokens:
            self.add_word(key,token)

    def add_word(self,key,word):
        self.word_graph.add_node(key, type='key')
        self.word_graph.add_node(word, type='word')
        self.add_or_inc_edge(key,word)
    
    def prune(self):
        self.word_graph=self.trim_edges(self.word_graph)
    
    def save(self):
        print "<<<<<<< SAVING WORD-GRAPH >>>>>>>"
        net.write_pajek(self.word_graph,"/tmp/egauge_wordgraph.net")
    
    def load(self):
        print "<<<<<<<< Loaing Word-Graph>>>>>>>"
        self.word_graph=net.read_pajek("/tmp/egauge_wordgraph.net")