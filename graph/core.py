#!/usr/bin/env python
#coding: utf8

from copy import copy

class CommonEqualityMixin(object):
    """describes common equality operations"""
    
    def __eq__(self, other):
        """equals"""
        return (isinstance(other, self.__class__)
            and self.__dict__ == other.__dict__)

    def __ne__(self, other):
        """not equals"""
        return not self.__eq__(other)

class Vertex(CommonEqualityMixin):
    """a vertex of a graph"""
    def __init__(self, label):
        self.__label = label
    
    def get_label(self):
        return self.__label
    
    def __str__(self):
        return "["+str(self.__label)+"]"
                
class Path(CommonEqualityMixin):
    """a trajectory within the graph"""
    
    def __init__(self, length, vseq):
        self.__length = length
        self.__sequence = vseq
    
    def get_length(self):
        return self.__length
    
    def get_sequence(self):
        return self.__sequence
        
    def __str__(self):
        l = str(self.__length)
        p = "->".join((str(x) for x in self.get_sequence()))
        return l + " " + p
        
class Graph(CommonEqualityMixin):
    """A graph that contains bonds and vertexes"""
    
    def __init__(self):
        self.__vertexes = []
        self.__bonds = {}
        
    def get_vertexes(self):
        return self.__vertexes
    
    def get_bonds(self):
        return self.__bonds
    
    def create_vertex(self):
        """creates vertex and adds it to graph"""
        vertex = Vertex(chr(97 + len(self.__vertexes)))
        self.get_vertexes().append(vertex)
        return vertex
    
    def add_bond(self, begin, end, length):
        """creates bond and adds it to graph"""
        if(not self.get_bonds().has_key(begin)):
            self.get_bonds()[begin] = []
        self.get_bonds()[begin].append((end, length))
        
    def get_bond_length(self, begin, end):
        """finds the length of the bond which connects two vertexes"""
        if(not self.get_bonds().has_key(begin)):
            return 0
        for current, length in self.get_bonds()[begin]:
            if(current == end):
                return length
        return 0 
    
    def find_closest_way(self, begin, end):
        """
            finds the closest ways between two vertexes
            begin -- vertex, where path is beginning
            end -- vertex, where path is ending
        """
        if(begin == end):
            empty = Path(0, [])
            return empty
        meter = dict((v, Path(10**6, [])) for v in self.get_vertexes()) 
        meter[begin] = Path(0, [begin])
        visited = []
        to_visit = []
        to_visit.append(begin)
        while(len(to_visit) > 0):
            position = to_visit.pop()
            visited.append(position)
            candidates = self.visit_vertex(meter, position)
            for c in (x for x in candidates if x not in visited):
                to_visit.append(c)
        return meter[end]
            
    def visit_vertex(self, meter, position):
        """
            visits the vertex and refreshes the meter
            meter -- the vector of the closest paths
            position -- the vertex to visit
        """
        to_visit = []
        cur_path = meter[position]
        distance = cur_path.get_length()
        for v in (x for x in self.get_vertexes() if self.get_bond_length(position, x) != 0):
            to_go = self.get_bond_length(position, v)
            to_visit.append(v)
            if(meter[v].get_length() > distance + to_go):
                sequence = copy(cur_path.get_sequence())
                sequence.append(v)
                meter[v] = Path(distance + to_go, sequence)
        return to_visit

    