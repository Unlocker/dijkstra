#!/usr/bin/env python
#coding: utf8

import unittest
from graph.core import Graph

class Test(unittest.TestCase):

    def test_create_vertex(self):
        # given
        graph = Graph()
        # when
        v = graph.create_vertex()
        # then
        self.assertEquals('a', v.get_label())
        

    def test_short_circuit(self):
        # given
        graph = Graph()
        v = graph.create_vertex()
        # when
        p = graph.find_closest_way(v, v)
        # then
        self.assertEquals(0, p.get_length())
        self.assertEquals(0, len(p.get_sequence()))
        
    def test_bond_length(self):
        # given
        graph = Graph()
        v = graph.create_vertex()
        e = graph.create_vertex()
        s = graph.create_vertex()
        # when
        graph.add_bond(v, e, 5)
        graph.add_bond(v, s, 3)
        # then
        self.assertEquals(0, graph.get_bond_length(s, v))
        self.assertEquals(5, graph.get_bond_length(v, e))
        self.assertEquals(3, graph.get_bond_length(v, s))
    
    # [a] =5=> [b]    
    def test_two_vertexes(self):
        # given
        graph = Graph()
        a = graph.create_vertex()
        b = graph.create_vertex()
        graph.add_bond(a, b, 5)
        # when
        p = graph.find_closest_way(a, b)
        # then
        self.assertEquals(5, p.get_length())
        self.assertIn(a, p.get_sequence())
        self.assertIn(b, p.get_sequence())
        print p
    
    # [a]=3=>[b]=2=>[c]=1=>[e]
    #    \\               /^ 
    #      ===5=>[d]==2===
    def test_many_vertexes(self):
        # given
        graph = Graph()
        a = graph.create_vertex()
        b = graph.create_vertex()
        c = graph.create_vertex()
        d = graph.create_vertex()
        e = graph.create_vertex()
        graph.add_bond(a, b, 1)
        graph.add_bond(b, c, 2)
        graph.add_bond(c, e, 3)
        graph.add_bond(a, d, 5)
        graph.add_bond(d, e, 2)
        # when
        p = graph.find_closest_way(a, e)
        # then
        self.assertEquals(6, p.get_length())
        self.assertEquals(4, len(p.get_sequence()))
        self.assertIn(b, p.get_sequence())
        self.assertIn(c, p.get_sequence())
        print p
        
    # [a]=3=>[b]=6=>[c]=1=>[e]
    #    \\               /^ 
    #      ===5=>[d]==2===
    def test_another_graph(self):
        # given
        graph = Graph()
        a = graph.create_vertex()
        b = graph.create_vertex()
        c = graph.create_vertex()
        d = graph.create_vertex()
        e = graph.create_vertex()
        graph.add_bond(a, b, 1)
        graph.add_bond(b, c, 6)
        graph.add_bond(c, e, 3)
        graph.add_bond(a, d, 5)
        graph.add_bond(d, e, 2)
        # when
        p = graph.find_closest_way(a, e)
        # then
        self.assertEquals(7, p.get_length())
        self.assertEquals(3, len(p.get_sequence()))
        self.assertIn(d, p.get_sequence())
        print p

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()