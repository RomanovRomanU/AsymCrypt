# from generators import BM_bit
from math import gcd
from random import randrange
from gmpy2 import mpz, powmod, is_prime



class BM:
    def __init__(self,T0):
        self.name = "BM"
        self.T = mpz(T0)
        self.p = mpz(0xCEA42B987C44FA642D80AD9F51F10457690DEF10C83D0BC1BCEE12FC3B6093E3)
        self.a = mpz(0x5B88C41246790891C095E2878880342E88C79974303BD0400B090FE38A688356)
        self.threshold = (self.p - 1)/2

    def __next__(self):
        T_new = powmod(self.a,self.T,self.p)
        self.T = T_new

    def get_state(self):
        if self.T < self.threshold:
            return 1
        else:
            return 0
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


def generate_number(bit_length, start_state=0x56AA, generator=BM_bit):
    generator = generator(start_state)
    result = ''
    for i in range(bit_length):
        next(generator)
        result += str(generator.get_state())
    return int(result, 2)

def number_decomposition(number):
    '''
    Represent number like this:
    number = d * (2**s), where
    d - odd number
    '''
    s = 0
    while number % 2 == 0:
        number = number // 2
        s += 1
    d = number
    return (d,s)

def check_prime(p, k=25):
    '''
    Miller-Rabin primality test
    p - number, which primality we check
    k - number of iterations in test
    '''
    d, s = list(map(int, number_decomposition(p - 1)))
    for _ in range(k):
        x = randrange(2,p)
        if gcd(x, p) == 1:
            y = powmod(x,d,p)      
            # Значит число сильно псевдопростое по основанию
            if y in [1, p-1]:
                continue
            else:
                for r in range(1,s):
                    y = powmod(y,2,p)
                    # Число сильно псевдопростое
                    if y == -1:
                        break
                    # Число не сильно псевдопростое(а значит и не простое)
                    if y == 1:
                        return False
                # Если за весь цикл не смогли доказать
                # псевдопростоту, то оно не псевдопростое
                return False
        else:
            # p is not prime
            return False
    # Если оно было пседопростое по всем k случайныи основаниям
    return True

def generate_prime(bit_length):
    new_number = generate_number(bit_length, start_state=randrange(mpz(0xCEA42B987C44FA642D80AD9F51F10457690DEF10C83D0BC1BCEE12FC3B6093E3)))
    while not is_prime(new_number):
        new_number = generate_number(bit_length, start_state=randrange(mpz(0xCEA42B987C44FA642D80AD9F51F10457690DEF10C83D0BC1BCEE12FC3B6093E3)))
    return new_number

def generate_mutually_simple(n):
    k = randrange(2,n)
    while gcd(k, n) != 1:
        k = randrange(2,n)
    return k

# Extended GCD algorithm
# ax + by = gcd
def xgcd(b, n):
    x0, x1, y0, y1 = 1, 0, 0, 1
    while n != 0:
        q, b, n = b // n, n, b % n
        x0, x1 = x1, x0 - q * x1
        y0, y1 = y1, y0 - q * y1
    return  b, x0, y0

class RsaUser:
    def __init__(self, bit_length=300):
        '''
        n и e - публичные ключи
        d - секретный ключ
        p, q - тоже секрет
        '''
        self.p = generate_prime(bit_length)
        self.q = generate_prime(bit_length)
        while self.q == self.p:
            self.q = generate_prime(bit_length)

        self.n = self.p * self.q
        phi_n = (self.p - 1)*(self.q - 1)
        self.e = generate_mutually_simple(phi_n)
        # e*d = 1(mod(phi_n))
        # Вот тут могуть быть баги
        self.d_ = xgcd(self.e, phi_n)[1]

    def encrypt(self, M):
        # C = (M**e) mod n
        return powmod(M, self.e, self.n)

    def decrypt(self, C):
        # M = (C**d) mod n
        return powmod(C, self.d_, self.n)

    # Цифровая подпись
    def sign(self, M):
        S = powmod(M, self.d_, self.n)
        return (M, S)

    def verify_sign(self,M,S):
        if M == powmod(S, self.e, self.n):
            return True
        else:
            return False

    def send_message(self, key, other_user):
        other_user.recieve_message(key)

    def recieve_message(self,key):
        self.oher_user_message = key

    # Ключ, который мы хотим передать
    def generate_k(self):
        self.k = randrange(1,self.n)

    # Сообщение для другого обонента при обмене ключами,
    # и его передача
    def send_key(self, other_user):
        k1 = powmod(self.k, other_user.e, other_user.n)
        s = powmod(self.k, self.d_, self.n)
        s1 = powmod(s, other_user.e, other_user.n)
        return (k1, s1)

    def process_other_user_key(self, key, other_user):
        k1 = key[0]
        s1 = key[1]

        k = powmod(k1, self.d_, self.n)
        s = powmod(s1, self.d_, self.n)

        # Process of sign check
        if k == powmod(s, other_user.e, other_user.n):
            print(k)
            print('Обмен ключами состоялся!')



def rsa_protocol():
    '''
    Хотим передать значение
    0 < k < n , которое будет секретным
    '''
    alice = RsaUser()
    bob = RsaUser()
    # Open key of Alice
    e = alice.e
    n = alice.n
    # Open key of Bob
    e1 = bob.e
    n1 = bob.n

    if e == e1 or n == n1:
        return rsa_protocol()
    # Если такое условие не выполняется,
    # то генерим другие пары ключей
    if bob.n < alice.n:
        return rsa_protocol()

    # Алиса генерит ключ k, который хочет передать Бобу
    alice.generate_k()
    print(alice.k)
    bob.process_other_user_key(alice.send_key(bob), alice)






if __name__ == "__main__":
    '''
    alice = RsaUser()
    # Проверка зашифрования-расшифрования
    ciphertext = alice.encrypt(11111111111111111111111111111111111111111111111111)
    print(ciphertext)
    print(alice.decrypt(ciphertext))
    # Проверка цифровой подписи
    M,S = alice.sign(0xAAAA)
    print(alice.verify_sign(M,S))
    '''
    rsa_protocol()