from lab2_RSA import generate_prime
from math import ceil
from random import randrange
from gmpy2 import mpz, powmod, gcdext, f_mod
from pyfac import jacobi


class RabinUser(object):
    def __init__(self, bit_length):
        # p and q - not equal blum numbers (secret)
        self.p_ = self.generate_blum_number(bit_length)
        self.q_ = self.generate_blum_number(bit_length)
        while self.p_ == self.q_:
            self.q_ = self.generate_blum_number(bit_length)

        # Public key
        self.n = self.p_ * self.q_

    @staticmethod
    def generate_blum_number(bit_length):
        # Blum number: prime number of type 4k+3
        number = generate_prime(bit_length)
        # Check if it`s 4k+3 number
        while number % 4 != 3:
            number = generate_prime(bit_length)

        return number

    @staticmethod
    def get_bit_length(number):
        bit_length = 0
        while number != 0:
            number = number >> 1
            bit_length += 1
        return bit_length

    @staticmethod
    def get_byte_length(number):
        return ceil(RabinUser.get_bit_length(number) / 8)

    # Find x = y**2 (mod n)
    # For case, when n = p*q
    # p,q - Blum numbers
    @staticmethod
    def sqrt(y, p, q):
        n = p * q
        p1 = mpz((p + 1) / 4)
        q1 = mpz((q + 1) / 4)
        s1 = powmod(y, p1, p)
        s2 = powmod(y, q1, q)
        u, v = gcdext(p, q)[1:]
        # Result is: (+/-)*u*p*s1 + (+/-)*v*p*s2
        result = []
        for first_sign in [1, -1]:
            for second_sign in [1, -1]:
                local_result = \
                    (first_sign * u * p * s1) + (second_sign * v * q * s2)
                result.append(f_mod(local_result, n))
        return result

    def format_message(self, m):
        # m - message
        # Number of bytes in n
        l = RabinUser.get_byte_length(self.n)
        # Random 64-bit number for formating
        r = randrange(1, 2 ** 64)
        # Formated message
        x = 255 * (2 ** (8 * (l - 8))) + m * (2 ** 64) + r
        return x

    def encrypt_message(self, message):
        x = self.format_message(message)
        print('x is:',x)
        y = powmod(x, 2, self.n)
        print('y is', y)
        print('n is', self.n)
        # Indicator of even number
        c1 = x % 2
        # Indicator of: (x/n) = 1
        # (x/n) - Jacobi symbol
        c2 = 1 if jacobi(x, self.n) == 1 else 0
        return y

    def decrypt_message(self, decrypted_message):
        pass


if __name__ == '__main__':
    x = RabinUser(128)
    p = x.p_
    q = x.q_

    m = 1234
    cipher = x.encrypt_message(m)

    print(x.sqrt(cipher,p,q))
    # print(x.format_message(123456))
    # print(x.generate_blum_number(20))