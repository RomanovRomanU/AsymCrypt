# -*- coding: utf-8 -*-
import re
from complex_generators import L89,L9,L11,L10,Geffe,L20
import numpy as np
from time import time
from random import randrange
from gmpy2 import mpz, powmod

def clear_text(string):
	#substituting bad symbols
	string = string.lower()
	string = re.sub(r"\.|\"|\(|\)|\?|\'|\d|\t|\<|\>|\*|\\|\n"," ",string)
	string = re.sub(r"[qwertyuiopasdfghjklzxcvbnm:!,-;=^]"," ",string)
	string = re.sub(r" +"," ",string)
	string = string.replace('ъ','ь')
	string = string.replace('ё','е')
	string = string.replace(' ','')
	return string

class BasicGenerator():
    def __init__(self):
        self.name = "Basic Generator"
    def get_octal_state(self):
        return randrange(0,256)
    def name(self):
        return self.name

class LemerGenerator():
    def __init__(self, a, c, m, state):
        self.name = "Lemmer"
        self.a = a
        self.c = c
        self.m = m
        self.state = state
    def __iter__(self):
        return self
    def __next__(self):
        new_element = (self.a * self.state + self.c) % self.m
        self.state = new_element
        return self.state
    def name(self):
        return self.name

# Done
class LemerLow(LemerGenerator):
    def get_octal_state(self):
        next(self)
        bin_state = bin(self.state)[-8:]
        return int(bin_state,2)

# Done
class LemerHigh(LemerGenerator):
    def get_octal_state(self):
        next(self)
        bin_state = bin(self.state)[2:]
        nulls = "0" * (32 - len(bin_state))
        bin_state = (nulls + bin_state)[0:8]
        return int(bin_state,2)

# Done
class Wolfram:
    def __init__(self,state):
        self.name = "Wolfram"
        self.state = state
    def __next__(self):
        r = self.state
        r = (((r << 1) | (r >> 31)) & (2**32 - 1))^(r | (((r >> 1) | (r << 31)) & (2**32 - 1)))
        self.state = r
    def get_state(self):
        return self.state % 2

    def get_octal_state(self):
        result = ''
        for i in range(8):
            next(self)
            result += str(self.get_state())
        return int(result, 2)

    def name(self):
        return self.name

class Librarian:
    def __init__(self):
        self.name = "Librarian"
        book = open('Voyna_i_mir.txt','r')
        self.sequence = bytes(clear_text(book.read()),'utf-8')
        self.index = 0
    def __next__(self):
        self.index += 1
    def get_octal_state(self):
        next(self)
        return self.sequence[self.index]
    def name(self):
        return self.name

class BM:
    def __init__(self,T0):
        self.name = "BM"
        self.T = mpz(T0)
        self.p = mpz(0xCEA42B987C44FA642D80AD9F51F10457690DEF10C83D0BC1BCEE12FC3B6093E3)
        self.a = mpz(0x5B88C41246790891C095E2878880342E88C79974303BD0400B090FE38A688356)
        self.threshold = (self.p - 1)/2

    def __next__(self):
        T_new = powmod(self.a,self.T,self.p)
        # T_new = (self.a**self.T) % self.p
        self.T = T_new

    def get_state(self):
        if self.T < self.threshold:
            return 1
        else:
            return 0
    # Вот это оооочень неоптимизировано
    def get_octal_state(self):
        next(self)
        return (256 * self.T)//(self.p - 1)
    def name(self):
        return self.name

class BM_bit(BM):
    def get_octal_state(self):
        result = ''
        for i in range(8):
            next(self)
            result += str(self.get_state())
        return int(result, 2)

class BBS:
    def __init__(self, r0):
        self.name = "BBS"
        if r0 < 2:
            raise AttributeError('r0 must be >= 2')
        self.r = r0
        self.p = 0xD5BBB96D30086EC484EBA3D7F9CAEB07
        self.q = 0x425D2B9BFDB25B9CF6C416CC6E37B59C1F
        self.n = self.p * self.q

    def __next__(self):
        r_new = (self.r ** 2) % self.n
        self.r = r_new

    def get_state(self):
        return (self.r & 1)

    def get_octal_state(self):
        next(self)
        return (self.r & 0xFF)
    def name(self):
        return self.name

class BBS_bit(BBS):
    def get_octal_state(self):
        result = ''
        for i in range(8):
            next(self)
            result += str(self.get_state())
        return int(result, 2)

# Генератор должен возвращать байты
# z = Z(1-альфа)
def equability_check(generator,iterations,z):
    values_frequency = dict()
    for _ in range(iterations):
        value = generator.get_octal_state()
        if values_frequency.get(value):
            values_frequency[value] += 1
        else:
            values_frequency[value] = 1
    # Хи**2
    criteria = 0
    n = iterations / 256
    for i in range(256):
        criteria += (values_frequency.get(i,0) - n)**2 / n
    # Хи**2  (1-альфа)
    l = 255
    limit_criteria = ((2*l)**(1/2)) * z + l
    print('%s -- %s -- %s, Passing: %s' % (
        generator.__class__.__name__, criteria, limit_criteria, criteria <= limit_criteria
    ))
    return criteria <= limit_criteria

def independence_check(generator,iterations,z):
    values_frequency = [[0 for i in range(256)] for i in range(256)]
    for _ in range(0,iterations,2):
        first_value = generator.get_octal_state()
        second_value = generator.get_octal_state()
        values_frequency[first_value][second_value] += 1

    # Chi ** 2
    criteria = 0
    n = 0
    for i in range(256):
        for j in range(256):
            pair_amount = values_frequency[i][j]
            if pair_amount == 0:
                continue
            n += pair_amount
            first_value_amount = sum([values_frequency[i][k] for k in range(256)])
            second_value_amount = sum([values_frequency[k][j] for k in range(256)])
            # Избегаем деления на ноль
            criteria += (pair_amount ** 2)/(first_value_amount * second_value_amount)
    criteria = n* (criteria - 1)
    l = 255 ** 2
    limit_criteria = ((2*l)**(1/2)) * z + l
    print('%s -- %s -- %s, Passing: %s' % (
        generator.__class__.__name__, criteria, limit_criteria, criteria <= limit_criteria
    ))
    return criteria <= limit_criteria

# r - число отрезков,на которые разбиваем
def uniformity_check(generator,iterations,z,r = 20):
    values_frequency = [[0 for i in range(256)] for j in range(r)]
    cut_length = iterations // r
    # По всем отрезкам
    for j in range(r):
        # Генерим значение на отрезке
        for _ in range(cut_length):
            value = generator.get_octal_state()
            values_frequency[j][value] += 1
    criteria = 0
    for i in range(256):
        for j in range(r):
            byte_on_cut_amount = values_frequency[j][i]
            if byte_on_cut_amount == 0:
                continue
            byte_amount = sum([values_frequency[k][i] for k in range(r)])
            # У нас длинна отрезков везде одинаковая, поэтому её не считаем

            criteria += (byte_on_cut_amount ** 2) / (byte_amount * cut_length)
    n = r * cut_length
    criteria = n * (criteria - 1)

    # Chi (1-alpha) ** 2
    l = 255 * (r - 1)
    limit_criteria = ((2*l)**(1/2)) * z + l
    print('%s -- %s -- %s, Passing: %s' % (
        generator.__class__.__name__, criteria, limit_criteria, criteria <= limit_criteria
    ))
    return criteria <= limit_criteria

# Key is alpha - value is Z(1-alpha)
Z = {
    0.01: 2.32,
    0.05: 1.64,
    0.1: 1.28
}


# --------------------------------------------------------------
# For LemmerLow and LemmerHigh
m = 1<<32
a = (1<<16) + 1
c = 119
if __name__ == "__main__":
    #basic = BasicGenerator()
    #l20 = L20()
    #lemer_low = LemerLow(a,c,m,123)
    #lemer_high = LemerHigh(a,c,m,123)
    #x = L11()
    #y = L9()
    #s = L10()
    #geffe = Geffe(x,y,s)
    #wolfram = Wolfram(65)
    #librarian = Librarian()
    #bm = BM(0x7877)
    #bm_bit = BM_bit(0x56AA)
    #bbs = BBS(0xAAAA)
    #bbs_bit = BBS_bit(0xFF123)
    #Вот тут еще должно быть bm_bit, bbs_bit

    #uniformity_check(librarian,1000000,Z[0.01])
    #generators = [basic,l20,l89,lemer_low,lemer_high,geffe,wolfram,librarian,bm,bbs,bm_bit,bbs_bit]
    #for generator in generators:
    #    z = Z[0.1]
    #    uniformity_check(generator,1000000,z)
    #    print('----------------------------------')

    #l89 = L89()
    #equability_check(l89,1000000,Z[0.01])
    #uniformity_check(l89,1000000,Z[0.01])

    #equability_check(wolfram,1000000,Z[0.01])
    #wolfram = Wolfram(0xAAAA)
    #independence_check(wolfram,1000000,Z[0.01])
    #uniformity_check(wolfram,1000000,Z[0.01])

    librarian = Librarian()
    #equability_check(librarian,1000000,Z[0.01])
    #independence_check(librarian,100000,Z[0.01])
    uniformity_check(librarian,1000000,Z[0.01],r=20)
