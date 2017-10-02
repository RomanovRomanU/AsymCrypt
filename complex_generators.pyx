from cpython cimport bool
import numpy as np

def left_shift(number):
    rest = number >> 31
    if rest == 1:
        return (number << 1) | 1
    else:
        return number << 1

def rigth_shift(number):
    rest = number & 1
    if rest == 1:
        return (number >> 1) | (rest << 31)
    else:
        return number >> 1

cdef class L89:
    cdef int[89] state
    def __init__(self,start_state = None):
        if type(start_state) == list and len(start_state) == 89:
            self.state = start_state
        else:
            self.state = [1 for i in range(89)]
    def __next__(self):
        cdef int new_element
        new_element = self.state[0] ^ self.state[51]
        cdef int i
        for i in range(1,len(self.state)):
            self.state[i-1] = self.state[i]
        self.state[len(self.state) - 1] = new_element
        return new_element
    def get_state(self):
        return self.state

cdef class L9:
    cdef int[9] state
    def __init__(self,start_state = None):
        if type(start_state) == list and len(start_state) == 9:
            self.state = start_state
        else:
            self.state = [1 for i in range(9)]
    def __next__(self):
        cdef int new_element
        new_element = self.state[0]^self.state[1]^self.state[3]^self.state[4]
        for i in range(1,len(self.state)):
            self.state[i-1] = self.state[i]
        self.state[len(self.state) - 1] = new_element
        return new_element
    def get_state(self):
        return self.state

cdef class L10:
    cdef int[10] state
    def __init__(self,start_state = None):
        if type(start_state) == list and len(start_state) == 10:
            self.state = start_state
        else:
            self.state = [1 for i in range(10)]
    def __next__(self):
        cdef int new_element
        new_element = self.state[0]^self.state[3]
        for i in range(1,len(self.state)):
            self.state[i-1] = self.state[i]
        self.state[len(self.state) - 1] = new_element
        return new_element
    def get_state(self):
        return self.state

cdef class L11:
    cdef int[11] state
    def __init__(self,start_state = None):
        if type(start_state) == list and len(start_state) == 11:
            self.state = start_state
        else:
            self.state = [1 for i in range(11)]
    def __next__(self):
        cdef int new_element
        new_element = self.state[0]^self.state[2]
        for i in range(1,len(self.state)):
            self.state[i-1] = self.state[i]
        self.state[len(self.state) - 1] = new_element
        return new_element
    def get_state(self):
        return self.state

cdef class Geffe:
    cdef L11 x
    cdef L9 y
    cdef L10 s
    def __init__(self,x,y,s):
        self.x = x
        self.y = y
        self.s = s

    def __next__(self):
        cdef int x_new = next(self.x)
        cdef int y_new = next(self.y)
        cdef int s_new = next(self.s)
        return s_new&x_new ^ (1^s_new) & y_new

cdef class Wolfram:
    cdef int state
    def __init__(self,state):
        self.state = state

    def __next__(self):
        cdef unsigned int new_state
        new_state = left_shift(self.state) ^ (self.state | rigth_shift(self.state))
        self.state = new_state

    def get_state(self):
        return self.state & 1

