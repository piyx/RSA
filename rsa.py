from math import sqrt
import os
import random


LOWER_LIMIT = 10**5
UPPER_LIMIT = 10**7


def isprime(n: int) -> bool:
    '''Check whether a number is prime or not

    Example:

        >>> isprime(37)
        True
        >>> isprime(201) 
        False

    '''
    if n <= 3: return n > 1
    if n%2 == 0: return False
    if n%3 == 0: return False

    for i in range(5, int(sqrt(n))+1, 6):
        if n%i == 0 or n%(i+2) == 0:
            return False
    
    return True


def random_prime(lo: int, hi: int) -> int:
    '''Returns a random prime number in the range [lo, hi] inclusive

    Example:
        >>> random_prime(10**5, 10**7) 
        6343417
        >>> random_prime(100, 1000)
        809
        >>> random_prime(10, 20) 
        11

    '''
    n = random.randint(lo, hi)
    
    while not isprime(n):
        n = random.randint(lo, hi)
    
    return n


def generate_prime_pair(lo: int, hi: int) -> tuple[int, int]:
    '''Generates 2 non equal prime numbers in the range [lo, hi]

    Example:
        >>> generate_prime_pair(100, 200) 
        (173, 113)
        >>> generate_prime_pair(1000, 2000) 
        (1451, 1997)
    
    '''
    p = random_prime(lo, hi)
    q = random_prime(lo, hi)
    
    while q == p:
        q = random_prime(lo, hi)

    return p, q


def gcd(n: int, m: int) -> int:
    '''Computes the GCD of n and m

    Example:
        >>> gcd(11, 13) 
        1
        >>> gcd(12, 18) 
        6
        
    '''
    while m:
        n, m = m, n%m
    
    return n


class RSA:
    '''
    Properties

    p: int -> prime p
    q: int -> prime q
    n: int -> modulus
    e: int -> public exponent
    d: int -> modular multiplicative inverse

    => Note: p != q
    => n = pq // n is the modulus  
    => phi = (p-1) * (q-1) // phi(n) is the totient of n
    => 1 < e < phi and gcd(e, phi) = 1 // e and phi are coprime
    => de = 1 mod phi (or) d = e^-1 mod phi 
    '''
    @staticmethod
    def generatekeys() -> tuple[tuple]:
        '''Returns a key pair (Public key and Private key)'''
        p, q = generate_prime_pair(LOWER_LIMIT, UPPER_LIMIT)
        n = p*q
        phi = (p-1) * (q-1)
        e = random.randrange(1, phi)
        while gcd(e, phi) != 1:
            e = random.randrange(1, phi)
        
        d = pow(e, -1, phi)

        return ((e, n), (d, n))

    
    @staticmethod
    def encrypt(filename: str, publickey: tuple[int, int]) -> None:
        '''Encrypts the contents of the file using the public key'''

        if not os.path.exists(filename):
            raise FileNotFoundError(f"{filename} not found")

        e, n = publickey
        
        # Consumes the whole content and stores in memory
        # Not ideal for large files
        with open(filename) as f:
            contents = f.read()
        
        encrypted_data = []
        with open(filename, 'w') as f:
            for char in contents:
                encrypted_char = pow(ord(char), e, n)
                encrypted_data.append(encrypted_char)
            
            f.write(' '.join(map(str, encrypted_data)))


    @staticmethod
    def decrypt(filename: str, privatekey: tuple[int, int]) -> None:
        '''Decrypts the contents of the file using the private key'''
    
        if not os.path.exists(filename):
            raise FileNotFoundError(f"{filename} not found")

        d, n = privatekey

        with open(filename) as f:
            encrypted_contents = f.read().split()
        
        decrypted_data = []
        with open(filename, 'w') as f:
            for num in map(int, encrypted_contents):
                decrypted_char = chr(pow(num, d, n))
                decrypted_data.append(decrypted_char)
            
            f.write(''.join(map(str, decrypted_data)))