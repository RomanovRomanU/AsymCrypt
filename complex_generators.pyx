from cpython cimport bool, str
import numpy as np

# Done
cdef class L89:
    cdef int[89] state
    cdef public str name
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

    def get_octal_state(self):
        result = ''
        for i in range(8):
            result += str(next(self))
        return int(result, 2)

    def name(self):
        return self.name

# Done
cdef class L9:
    cdef int[9] state
    cdef public str name
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

    def get_octal_state(self):
        result = ''
        for i in range(8):
            result += str(next(self))
        return int(result, 2)

    def name(self):
        return self.name

# Done
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

    def get_octal_state(self):
        result = ''
        for i in range(8):
            result += str(next(self))
        return int(result, 2)

# Done
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

    def get_octal_state(self):
        result = ''
        for i in range(8):
            result += str(next(self))
        return int(result, 2)


cdef class L20:
    cdef int[20] state

    def __init__(self,start_state = None):
        if type(start_state) == list and len(start_state) == 20:
            self.state = start_state
        else:
            self.state = [1 for i in range(20)]

    def __next__(self):
        cdef int new_element
        new_element = self.state[0]^self.state[11]^self.state[15]^self.state[17]
        for i in range(1,len(self.state)):
            self.state[i-1] = self.state[i]
        self.state[len(self.state) - 1] = new_element
        return new_element

    def get_state(self):
        return self.state

    def get_octal_state(self):
        result = ''
        for i in range(8):
            result += str(next(self))
        return int(result, 2)

# Done
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

    def get_octal_state(self):
        result = ''
        for i in range(8):
            result += str(next(self))
        return int(result, 2)


