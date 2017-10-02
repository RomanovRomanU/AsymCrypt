# -*- coding: utf-8 -*-
from bitarray import bitarray
from complex_generators import L89,L9,L11,L10,Geffe,Wolfram
import numpy as np

# For LemmerLow and LemmerHigh
m = 1<<32
a = (1<<16) + 1
c = 119
class LemerGenerator():
    def __init__(self, a, c, m, state):
        self.a = a
        self.c = c
        self.m = m
        self.state = state
    def __iter__(self):
        return self
    def __next__(self):
        new_element = (self.a * self.x_0 + self.c) % self.m
        self.state = new_element
        return self.state

class LemerLow(LemerGenerator):
    def get_state(self):
        bin_state = bin(self.state)[-16:]
        return bin_state[8:]

class LemerHigh(LemerGenerator):
    def get_state(self):
        bin_state = bin(self.state)[-16:]
        return bin_state[0:8]

class L20():
    # [x_0,x_1,...,x_n]
    def __init__(self, state):
        if len(state) > 20:
            raise ValueError("Your start state is not valid")
        self.state = bitarray(state) + bitarray([0 for i in range(20 - len(state))])
        self.start_state = state
    def __iter__(self):
        return self
    def __next__(self):
        state = self.state
        if state == self.start_state:
            raise StopIteration()
        new_element = state[0] ^ state[11] ^ state[15] ^ state[17]
        new_element = bitarray([new_element])
        self.state = state[1:] + new_element
        return self.state

class Librarian:
    def __init__(self):
        book = open('Повесть','r')
        self.sequence = bytes(book,'utf')
        self.index = 0
    def __next__(self):
        self.i += 1
    def get_state(self):
        return self.sequence[i]

class BM:
    def __init__(self,T0):
        pass
x = L11()
y = L9()
s = L10()
g = Geffe(x,y,s)




