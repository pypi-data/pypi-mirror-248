# -*- coding: utf-8 -*-
"""
Created on Thu Dec  2 11:43:37 2021

@author: Chai Wah Wu

functions to generate The On-Line Encyclopedia of Integer Sequences (OEIS) sequences

requires python >= 3.8

Usage:
Functions named Axxxxxx: Axxxxxx(n) returns the n-th term of OEIS sequence Axxxxxx
Functions named Axxxxxx_T: returns T(n,k) for OEIS sequences where the natural definition is a 2D table T.

For sequences where terms are best generated sequentially, a generator is provided.
Functions named Axxxxxxgen: Axxxxxxgen() returns a generator of OEIS sequence Axxxxxx
    For instance, list(islice(Axxxxxxgen(),10)) returns the first 10 terms of sequence Axxxxxx
    Alternatively, setting gen = Axxxxxxgen() and using next(gen) returns the next term.
    Given Axxxxxxgen, one can define Axxxxxx as: 
        def Axxxxxx(n,offset=1): return next(islice(Axxxxxxgen(),n-offset,None)) 
    where a(offset) is the first term returned by the generator, same as the offset in OEIS.
"""

from __future__ import print_function, division
import sys, bisect
from functools import lru_cache, reduce
from itertools import islice, count, product, permutations, takewhile, accumulate, combinations_with_replacement, \
        combinations, repeat, groupby, chain
from fractions import Fraction
from collections import Counter
from math import factorial, floor, comb, prod, isqrt
from operator import mul, xor
from re import finditer, split, sub
from sympy.core.numbers import igcdex
from statistics import pvariance
from sympy import factorint, divisors, integer_nthroot, divisor_sigma, nextprime, Matrix, divisor_count, \
                  isprime, prime, totient, sympify, primerange, primepi, composite, compositepi, \
                  factorial2, prevprime, primefactors, harmonic, multiplicity, n_order, primorial, \
                  sqrt, bernoulli, ff, sin, cos, tan, fibonacci, pi
from sympy.ntheory import mobius
from sympy.ntheory.factor_ import digits as sympydigits, udivisor_sigma, sieve, reduced_totient, core, antidivisors
from sympy.combinatorics.partitions import IntegerPartition
from sympy.utilities.iterables import partitions, multiset_permutations, multiset_combinations
from sympy.functions.combinatorial.numbers import stirling, bell
from sympy.ntheory.continued_fraction import continued_fraction_periodic
from gmpy2 import fac, popcount, is_prime, is_square, next_prime, c_divmod, digits as gmpy2digits
from num2words import num2words
if sys.version_info < (3,9):
    from sympy import lcm as sympylcm, gcd as sympygcd
    def gcd(*x):
        r = x[0]
        for y in x[1:]:
            r = sympygcd(r,y)
        return r
    def lcm(*x):
        r = x[0]
        for y in x[1:]:
            r = sympylcm(r,y)
        return r
else:
    from math import lcm, gcd
   
""" Utility functions """
def palQ(n,b): # check if n is a palindrome in base b
    s = sympydigits(n,b)[1:]
    return s == s[::-1]

def palQgen10(): 
    """ generator of palindromes in base 10 """
    yield 0
    for x in count(1):
        for y in range(10**(x-1),10**x):
            s = str(y)
            yield int(s+s[-2::-1])
        for y in range(10**(x-1),10**x):
            s = str(y)
            yield int(s+s[::-1])

def palQgen(b=10): # generator of palindromes in base b
    yield 0
    x = 1
    while True:
        n = b**(x-1)
        n2 = n*b
        for y in range(n,n2): # odd-length
            k, m = y//b, 0
            while k >= b:
                k, r = divmod(k,b)
                m = b*m + r
            yield y*n + b*m + k
        for y in range(n,n2): # even length
            k, m = y, 0
            while k >= b:
                k, r = divmod(k,b)
                m = b*m + r
            yield y*n2 + b*m + k
        x += 1

def paloddgen(l, b=10): 
    """ generator of odd-length palindromes in base b of length <= 2*l """
    if l > 0:
        yield 0
        for x in range(1, l+1):
            n = b**(x-1)
            n2 = n*b
            for y in range(n, n2):
                k, m = y//b, 0
                while k >= b:
                    k, r = divmod(k, b)
                    m = b*m + r
                yield y*n + b*m + k

def multiset_perm_count(x): 
    """ count the number of permutations in a multiset (from a list or tuple) """
    return factorial(len(x))//prod(factorial(d) for d in Counter(x).values())

def intpartitiongen(n, m): 
    """ generator of partition of n into m decimal digits, return as list of strings """
    return (''.join(str(d) for d in IntegerPartition(p).partition+[0]*(m-s)) for s, p in partitions(n, k=9, m=m, size=True))

@lru_cache(maxsize=None)
def intpartition(n, m): 
    """ partition of n into m decimal digits, return as list of strings """
    return tuple(intpartitiongen(n,m))

def partitionpairs(xlist):
    """ generator of all partitions into pairs and at most 1 singleton, returning the sums of the pairs """
    if len(xlist) <= 2:
        yield [sum(xlist)]
    else:
        m = len(xlist)
        for i in range(m-1):
            for j in range(i+1,m):
                rem = xlist[:i]+xlist[i+1:j]+xlist[j+1:]
                y = [xlist[i]+xlist[j]]
                for d in partitionpairs(rem):
                    yield y+d         

def integerlog(n, b): 
    """ computes largest integer k>=0 such that b^k <= n """
    kmin, kmax = 0, 1
    while b**kmax <= n:
        kmax *= 2
    while True:
        kmid = (kmax+kmin)//2
        if b**kmid > n:
            kmax = kmid
        else:
            kmin = kmid
        if kmax-kmin <= 1:
            break
    return kmin

def ispandigital(m,n): 
    """ return True iff m is pandigital in base n """
    s = set()
    while m > 0:
        m, b = divmod(m,n)
        if b in s:
            return False
        s.add(b)
    return True

def ispandigital0(m,n): 
    """ return (True, s) if m is pandigital in base n and (False, False) otherwise where s is true iff m has a zero digit """
    s = set()
    z = False
    while m > 0:
        m, b = divmod(m,n)
        if b in s:
            return False, False
        if b == 0:
            z = True
        s.add(b)
    return True, z

def intbase(dlist,b=10): 
    """ convert list of digits in base b to integer """
    y = 0
    for d in dlist:
        y = y*b + d
    return y

""" Lunar arithmetic """
def lunar_add(n,m):
    sn, sm = str(n), str(m)
    l = max(len(sn),len(sm))
    return int(''.join(max(i,j) for i,j in zip(sn.rjust(l,'0'),sm.rjust(l,'0'))))
def lunar_mul(n,m):
    sn, sm, y = str(n), str(m), 0
    for i in range(len(sm)):
        c = sm[-i-1]
        y = lunar_add(y,int(''.join(min(j,c) for j in sn))*10**i)
    return y

""" """

""" List of OEIS sequences """

def A349804(n): return int((lambda x: x+x[::-1])(''.join(str(d) for d in range(1,n+1))))
def A349805(n): return int((lambda x: x+x[::-1])(''.join(str(d) for d in range(1,n+1))))//11
def A173426(n): return int(''.join(str(d) for d in range(1,n+1))+''.join(str(d) for d in range(n-1,0,-1)))
def A349724(): # generator of terms
    for k in count(1):
        if not k*(k+1)//2 % prod(p**(e-1)*((p-1)*e+p) for p, e in factorint(k).items()): 
            yield k
def A018804(n): return prod(p**(e-1)*((p-1)*e+p) for p, e in factorint(n).items())
def A349711(n):
    f = factorint(n)
    plist, m = list(f.keys()), sum(f[p]*p for p in f)
    return sum((lambda x: x*(m-x))(sum(d[i]*p for i, p in enumerate(plist))) for d in product(*(list(range(f[p]+1)) for p in plist)))
def A349712(n):
    f = factorint(n)
    plist = list(f.keys())
    return sum(sum(int(d[i] > 0)*p for i, p in enumerate(plist))*sum(int(d[i] < f[p])*p for i, p in enumerate(plist)) for d in product(*(list(range(f[p]+1)) for p in plist)))
def A348169gen(): # generator of terms
    for n in count(1):
        for d in divisors(n,generator=False):
            x, x2 = 1, 1
            while 3*x2 <= d:
                y, y2 = x, x2
                z2 = d-x2-y2
                while z2 >= y2:
                    z, w = integer_nthroot(z2,2)
                    if w:
                        A = n//d
                        B, u = divmod(n,x*(y+z)+y*z)
                        if u == 0 and gcd(A,B) == 1:
                            yield n
                            break
                    y += 1
                    y2 += 2*y-1
                    z2 -= 2*y-1
                else:
                    x += 1
                    x2 += 2*x-1
                    continue
                break
            else:
                continue
            break
def A349680(n): return n+(n-1)*divisor_sigma(n,0)-divisor_sigma(n,1)
def A349643(n):
    plist, clist = [2], [1]
    for i in range(1,n+1):
        plist.append(nextprime(plist[-1]))
        clist.append((-1)**i*comb(n,i))
    while True:
        if sum(clist[i]*plist[i] for i in range(n+1)) == 0: return plist[0]
        plist = plist[1:]+[nextprime(plist[-1])]
def A349544helper_(k,n):
    if k == 0 and n == 0: return (x for x in (1,))
    if k < n: return (y*3 for y in A349544helper_(k,n-1))
    return (abs(x+y) for x in A349544helper_(k-1,n) for y in (2**n,-2**n))
def A349544(n): return min(A349544helper_(n, n))
def A348183(n): return Matrix(n,n,[pow(i+j,2,n) for i in range(n) for j in range(n)]).det()
def A348226(n): 
    """ code assumes n <= 63 or n is prime """
    if is_prime(n):
        return 2
    if n > 63:
        return "Error: n <= 63 or n is prime"
    p = 2
    while True:
        for i in range(n-1,1,-1):
            s = gmpy2digits(p,i)
            if not is_prime(int(s,n)):
                break
        else:
            return p
        p = next_prime(p)
def A349529(n): return len(list(filter(lambda x: x == 1, Counter(''.join(d) for d in permutations(bin(i)[2:] for i in range(1,n+1))).values()))) # ~~~~
def A066640gen(): return filter(lambda n: all(set(str(m)) <= {'1','3','5','7','9'} for m in divisors(n,generator=True)), count(1,2))
def A014261gen(): return filter(lambda n: set(str(n)) <= {'1','3','5','7','9'}, count(1,2))
def A117960gen(): return filter(lambda n: set(str(n)) <= {'1','3','5','7','9'}, (m*(m+1)//2 for m in count(0)))
def A349243gen(): return filter(lambda n: set(str(n*(n+1)//2)) <= {'1','3','5','7','9'}, count(0))
def A348162gen(): # generator of terms    
    s, n, m = '0', 1, 0
    while True:
        yield m
        n, m = n*2, int(s,4)+int(('02'*n)[:len(s)],4)
        s = format(m,'0'+str(n)+'b')
def A335567(n): 
    m = divisor_count(n)
    return (n-m)*(n-m+1)//2
def A349360(n): 
    m = divisor_count(n)
    return m*(m-n) + n*(n+1)//2
def A349460gen(): return filter(lambda n: set(str(n)) <= {'0','2','4'},(n*n for n in count(0)))
def A342975gen(): return filter(lambda n: set(str(n)) <= {'0','1','3'},(n**3 for n in count(0)))
def A050251(n): return 4*n if n <= 1 else 1+sum(1 for i in paloddgen((n+1)//2) if isprime(i))
def A229629gen(): # generator of terms
    n = 1
    while True:
        s, sn = str(n**n), str(n)
        l, ln = len(s), len(sn)
        if (ln-l) % 2 == 0 and s[l//2-ln//2:l//2+(ln+1)//2] == sn: yield n
        n += 1
def A347113gen(): # generator of terms
    j, nset, m = 2, {1}, 2
    yield 1
    while True:
        k = m
        while k == j or gcd(k,j) == 1 or k in nset:
            k += 1
        yield k
        j = k+1
        nset.add(k)
        while m in nset:
            m += 1
def A347313(n):
    p, gen = prime(n), A347113gen()
    for i in count(1):
        q = next(gen)
        if p == q: return i
def A179993gen(): # generator of terms
    for m in count(1):
        if all(isprime(m//a-a) for a in takewhile(lambda x: x*x <= m, divisors(m))):
            yield m     
def A349327gen(): # generator of terms
    n = 2
    while True:
        if isprime(n**2-2) and isprime (2*n**2-1): yield n
        n = nextprime(n)    
def A348784gen(): # generator of terms
    i = 1
    for m in A347113gen():
        if isprime(m):
            yield i
        i += 1
def A348158(n): return sum(set(map(totient,divisors(n,generator=True))))
def A348213(n): 
    c, k = 0, n 
    m = A348158(k)
    while m != k:
        k, m = m, A348158(m)
        c += 1
    return c
def A003434(n):
    c, m = 0, n
    while m > 1:
        c += 1
        m = totient(m)
    return c
def A013588(n):
    s, k = set(Matrix(n,n,p).det() for p in product([0,1],repeat=n**2)), 1
    while k in s:
        k += 1
    return k
def iteratedphi(n):
    m = n
    while m > 1:
        m = totient(m)
        yield m
def A092694(n): return prod(iteratedphi(n))
def A092693(n): return sum(iteratedphi(n))       
def A254007(n): return 1 if n == 0 else len(set(tuple(sorted(accumulate(d))) for d in product((-1,1),repeat=n-1)))
def A348780(n): return sum(islice(A347113gen(),n))
def A343878(n):
    k, c = 0, dict()
    while True:
        m, r = 0, 1
        while r > 0: 
            k += 1
            r = c.get(m,0)
            if n == r:
                return k
            c[r] = c.get(r,0)+1
            m += 1            
def A348781(n):
    k, s, c = 0, 0, dict()
    while True:
        m, r = 0, 1
        while r > 0: 
            k += 1
            if k > n:
                return s
            r = c.get(m,0)
            s += r
            c[r] = c.get(r,0)+1
            m += 1
def A172500(n): return sympify('0.['+str(n)+']').p
def A172502(n): return sympify('0.['+str(n)+']').q
def A348870(n): return (lambda m,r: r.p if m % 2 else r.q)(n,sympify('0.['+str((n+1)//2)+']')) # ~~~~
def A339665(n):
    ds = tuple(divisors(n, generator=True))
    return sum(sum(1 for d in combinations(ds,i) if n*i % sum(d) == 0) for i in range(1,len(ds)+1))
def A339453(n):
    m = lcm(*range(2,n+1))
    return sum(1 for i in range(1,n+1) for d in combinations((m//i for i in range(1,n+1)),i) if m*i % sum(d) == 0)
def A349148(n):
    k = lcm(*range(2,n+1))
    return sum(1 for d in combinations_with_replacement((k//d for d in range(1, n+1)), n) if sum(d) % k == 0)
def A349215(n):
    fs = factorint(n)
    return sum(a-1 for a in fs.keys())+prod(1+d for d in fs.values())
def A349214(n):
    p = list(primerange(2,n+1))
    return n-len(p)+sum(p)

@lru_cache(maxsize=None)
def A339508(n):
    nlist = [i for i in range(2,n) if i % 10 != 0]
    if n == 0 or n == 1:
        return 1
    c = A339508(n-1)
    if n % 10 != 0:
        sn = str(n)
        if sn == sn[::-1]:
            c += 1
        for i in range(1,len(nlist)+1):
            for d in combinations(nlist,i):
                s = str(prod(d)*n)
                if s == s[::-1]:
                    c += 1
    return c

@lru_cache(maxsize=None)
def A339484(n): return 1 if n == 1 else A339484(n-1)+sum(sum(d)+n==(i+1)**2 for i in range(1,n) for d in combinations(range(1,n),i))

def A348516(n):
    k, s = 1, gmpy2digits(n,3).rstrip('0')
    if s == '1' or s == '': return 1-len(s)
    m = int(s,3)
    mk = m
    while s.count('1') != s.count('2'): k += 1; mk *= m; s = gmpy2digits(mk,3)
    return k
def A349179gen(): # generator of terms
    c = 0
    for i in count(1):
        if (m := A339665(i)) > c:
            yield i
            c = m
def A349145(n): return sum(1 for d in product(range(1,n+1),repeat=n) if sum(Fraction(i+1,j) for i, j in enumerate(d)).denominator == 1)
def A349146(n):
    k = lcm(*range(2,n+1))
    dlist = tuple(k//d for d in range(1,n+1))
    return sum(multiset_perm_count(d) for d in combinations_with_replacement(range(1,n+1),n) if sum(dlist[e-1] for e in d) % k == 0)
def A348895(n):
    l, c, nmax, k = 9*n, 0, 0, 10**(n-1)
    while l > c:
        for p in intpartition(l, n):
            for q in multiset_permutations(p):
                w = int(''.join(q))
                if w >= k:
                    wr = w % l
                    if wr > c:
                        c = wr
                        nmax = w
                    if wr == c and nmax < w:
                        nmax = w
        l -= 1
    return nmax
def A348894(n):
    l, c, nmin, k = 9*n, 0, 10**n-1, 10**(n-1)
    while l > c:
        for p in intpartition(l, n):
            for q in multiset_permutations(p):
                w = int(''.join(q))
                if w >= k:
                    wr = w % l
                    if wr > c:
                        c = wr
                        nmin = w
                    if wr == c and nmin > w:
                        nmin = w
        l -= 1
    return nmin
def A348730(n):
    l, c, k = 9*n, 0, 10**(n-1)
    while l-1 > c:
        c = max(c,max(s % l for s in (int(''.join(q)) for p in intpartition(l,n) for q in multiset_permutations(p)) if s >= k))
        l -= 1
    return c
def A348706(n): return int(gmpy2digits(n,3).replace('0',''),3)
def A348651(n): return popcount(fac(fac(n)))
def A348658gen(): # generator of terms
    k = 1
    while True:
        a, b = divisor_sigma(k), divisor_sigma(k,0)*k
        c = gcd(a,b)
        n1, n2 = 5*(a//c)**2-4, 5*(b//c)**2-4
        if (integer_nthroot(n1,2)[1] or integer_nthroot(n1+8,2)[1]) and (integer_nthroot(n2,2)[1] or integer_nthroot(n2+8,2)[1]):
            yield k
        k += 1
def A108861gen(): # generator of terms
    k2, kf = 1, 1
    for k in count(1):
        k2 *= 2
        kf *= k
        if not sum(int(d) for d in str(k2*kf)) % k: yield k
def A244060(n): return sum(int(d) for d in str(factorial(2**n)))   
def A008906(n): return len(str(factorial(n)).rstrip('0'))
def A301861(n): return sum(int(d) for d in str(factorial(factorial(n))))
def A348446gen(): # generator of terms. Greedy algorithm.
    a = 1
    c, b = Counter(), 1
    while True:
        k, kb = 1, b
        while c[kb] >= kb:
            k += 1
            kb += b
        c[kb] += 1
        b = k
        a2 = k
        yield a-a2
        k, kb = 1, b
        while c[kb] >= kb:
            k += 1
            kb += b
        c[kb] += 1
        b = k
        a = k
def A348441gen(): # generator of terms
    yield 1
    c, p, a = 1, {1}, 1
    for i in count(3):
        n, na = 1, a
        while na in p:
            n += 1
            na += a
        p.add(na)
        a = n
        if c < n:
            c = n
            yield i
def A348247(n):
    c, b, p = Counter(), 1, prime(n)
    for i in count(1):
        k, kb = 1, b
        while c[kb] >= kb:
            k += 1
            kb += b
        if kb == p:
            return i
        c[kb] += 1
        b = k
def A348353gen(): # generator of terms.
    p, q, r = 2, 3, 5
    while True:
        if isprime(p*p+q+r) and isprime(p+q*q+r) and isprime(p+q+r*r):
            yield p
        p, q, r = q, r, nextprime(r)
def A307730gen(): # generator of terms. Greedy algorithm.
    c, b = Counter(), 1
    while True:
        k, kb = 1, b
        while c[kb] >= kb:
            k += 1
            kb += b
        c[kb] += 1
        b = k
        yield kb
def A348442gen(): # generator of terms
    yield 1
    c, p, a = 1, {1}, 1
    while True:
        n, na = 1, a
        while na in p:
            n += 1
            na += a
        p.add(na)
        a = n
        if c < na:
            c = na
            yield c
def A348443gen(): # generator of terms
    yield 1
    c, p, a = 1, {1}, 1
    for i in count(2):
        n, na = 1, a
        while na in p:
            n += 1
            na += a
        p.add(na)
        a = n
        if c < na:
            c = na
            yield i
def A348440gen(): # generator of terms
    yield 1
    c, p, a = 1, {1}, 1
    while True:
        n, na = 1, a
        while na in p:
            n += 1
            na += a
        p.add(na)
        a = n
        if c < n:
            c = n
            yield c  
def A088177gen(): # generator of terms
    yield 1
    yield 1
    p, a = {1}, 1
    while True:
        n = 1
        while n*a in p:
            n += 1
        p.add(n*a)
        a = n
        yield n  
def A088178gen(): # generator of terms
    yield 1
    p, a = {1}, 1
    while True:
        n, na = 1, a
        while na in p:
            n += 1
            na += a
        p.add(na)
        a = n
        yield na      
def A099378(n): return (lambda x, y: x//gcd(x,y*n))(divisor_sigma(n),divisor_sigma(n,0))
def A099377(n): return (lambda x, y: y*n//gcd(x,y*n))(divisor_sigma(n),divisor_sigma(n,0))
def A103339(n): return (lambda x, y: y*n//gcd(x,y*n))(udivisor_sigma(n),udivisor_sigma(n,0))
def A103340(n): return (lambda x, y: x//gcd(x,y*n))(udivisor_sigma(n),udivisor_sigma(n,0))
def A348411gen(): return filter((lambda n:(lambda x, y: 2*gcd(x,y*n)==x)(divisor_sigma(n),divisor_sigma(n,0))),count(1))
def A066411(n):
    b = [comb(n,k) for k in range(n//2+1)]
    return len(set((sum(d[i]*b[i] for i in range(n//2+1)) for d in partitionpairs(list(range(n+1))))))
def A348338(n):
    m, s = 10**n, set()
    for k in range(m):
        c, k2, kset = 0, k, set()
        while k2 not in kset:
            kset.add(k2)
            c += 1
            k2 = 2*k2 % m
        s.add(c)
    return len(s)
def A348339(n):
    m, s = 10**n, set()
    for k in range(m):
        c, k2, kset = 0, k, set()
        while k2 not in kset:
            kset.add(k2)
            c += 1
            k2 = k2*k2 % m
        s.add(c)
    return len(s)
def A260355_T(n, k): # compute T(n, k)
    if k == 1:
        return n*(n+1)//2
    ntuple, count = tuple(range(1, n+1)), n**(k+1)
    for s in combinations_with_replacement(permutations(ntuple, n), k-2):
        t = list(ntuple)
        for d in s:
            for i in range(n):
                t[i] *= d[i]
        t.sort()
        v = 0
        for i in range(n):
            v += (n-i)*t[i]
        if v < count:
            count = v
    return count
def A219032(n): 
    s = str(n*n)
    m = len(s)
    return len(set(filter(lambda x: integer_nthroot(x,2)[1], (int(s[i:j]) for i in range(m) for j in range(i+1,m+1)))))
def A348467(n): 
    s = str(factorial(n))
    m = len(s)
    return len(set(int(s[i:j]) for i in range(m) for j in range(i+1,m+1)))
def A120004(n): 
    s = str(n)
    m = len(s)
    return len(set(int(s[i:j]) for i in range(m) for j in range(i+1,m+1)))
def A348428gen(): # generator of terms
    for n in count(1):
        s = [int(d) for d in str(n)]
        m = len(s)
        if n == Matrix(m, m, lambda i, j: s[(i+j) % m]).det(): yield n
def A306853gen(): # generator of terms
    for n in count(1):
        s = [int(d) for d in str(n)]
        m = len(s)
        if n == Matrix(m, m, lambda i, j: s[(i-j) % m]).per(): yield n
def A219325gen(): # generator of terms
    for n in count(1):
        s = [int(d) for d in bin(n)[2:]]
        m = len(s)
        if n == Matrix(m, m, lambda i, j: s[(i-j) % m]).det():
            yield n
def A000108gen(): # generator of terms
    yield 1
    yield 1
    m = 1
    for n in count(1):
        m = m*(4*n+2)//(n+2)
        yield m
@lru_cache(maxsize=None)
def A000700(n): return 1 if n== 0 else sum((-1)**(k+1)*A000700(n-k)*prod((p**(e+1)-1)//(p-1) for p, e in factorint(k).items() if p > 2) for k in range(1,n+1))//n

def A010815(n):
    m = isqrt(24*n+1)
    return 0 if m**2 != 24*n+1 else ((-1)**((m-1)//6) if m % 6 == 1 else (-1)**((m+1)//6))
if sys.version_info >= (3,10):
    def A000120(n): return n.bit_count()
else:
    def A000120(n): return bin(n).count('1')
def A000110gen():
    yield 1
    yield 1
    blist, b = [1], 1
    while True:
        blist = list(accumulate([b]+blist))
        b = blist[-1]
        yield b
@lru_cache(maxsize=None)
def A000009(n): return 1 if n == 0 else A010815(n)+2*sum((-1)**(k+1)*A000009(n-k**2) for k in range(1,isqrt(n)+1))
def A007953(n): return sum(int(d) for d in str(n))
def A000984gen(): # generator of terms
    yield 1
    m = 1
    for n in count(0):
        m = m*(4*n+2)//(n+1)
        yield m
def A000578(n): return n**3
def A002808(n): return composite(n)
def A002808gen(): # generator of terms
    n, m = 3, 5
    while True:
        for i in range(n+1,m):
            yield i
        n, m = m, nextprime(m)
def A000961gen(): # generator of terms
    yield 1
    for n in count(2):
        if len(factorint(n)) == 1:
            yield n
def A002113gen(): # generator of terms
    for n in count(0):
        if str(n) == str(n)[::-1]: yield n
def A003415(n): return sum((n*e//p for p,e in factorint(n).items())) if n > 1 else 0        
def A000265(n):
    while not n % 2:
        n //= 2
    return n
def A001006gen(): # generator of terms
    yield 1
    yield 1
    m, k = 1, 1
    for n in count(2):
        m, k = k, (k*(2*n+1)+(3*n-3)*m)//(n+2)
        yield k
def A000166gen(): # generator of terms
    m, x = 1, 1
    for n in count(0):
        x, m = x*n + m, -m
        yield x
def A004086(n): return int(str(n)[::-1])       
def A001414(n): return sum(p*e for p,e in factorint(n).items()) 
def A002144gen():
    for n in count(1):
        p = prime(n)
        if not (p-1) % 4:
            yield p
def A002182gen(): # generator of terms     
     r = 0
     for i in count(1):
         if (d := divisor_count(i)) > r:
             r = d
             yield i
def A001700gen(): # generator of terms      
    b = 1
    for n in count(0):
        yield b
        b = b*(4*n+6)//(n+2)
def A003418(n): return prod(p**integerlog(n, p) for p in sieve.primerange(1, n+1))
def A000111gen(): # generator of terms
    yield 1
    yield 1
    blist = [1]
    for n in count(0):
        blist = list(reversed(list(accumulate(reversed(blist))))) + [0] if n % 2 else [0]+list(accumulate(blist))
        yield sum(blist)
def A014137gen(): return accumulate(A000108gen())
def A014138gen(): return (x-1 for x in A014137gen())
def A349866gen(): # generator of terms
    return filter(lambda m: sum(divisor_sigma(m) % d for d in divisors(m,generator=True)) == m, count(1))
def A005349gen(): return filter(lambda n: not n % sum((int(d) for d in str(n))), count(1))
def A002322(n): return reduced_totient(n)                                                       
def A006318gen(): # generator of terms
    m, k = 1, 2
    yield m
    yield k
    for n in count(3):
        m, k = k, (k*(6*n-9)-(n-3)*m)//n
        yield k
def A007913(n): return prod(p for p, e in factorint(n).items() if e % 2)
def A000178gen(): # generator of terms
    yield 1
    n, m = 1, 1
    for i in count(1):
        m *= i
        n *= m
        yield n
def A010888(n): return 1 + (n - 1) % 9
def A000523(n): return n.bit_length()-1       
def A000593(n): return prod((p**(e+1)-1)//(p-1) for p, e in factorint(n).items() if p > 2)
def A064413gen(): # generator of terms
    yield 1
    yield 2
    l, s, b = 2, 3, set()
    for _ in count(0):
        i = s
        while True:
            if not i in b and gcd(i,l) > 1:
                yield i
                l = i
                b.add(i)
                while s in b:
                    b.remove(s)
                    s += 1
                break
            i += 1  
def A006218(n): return 2*sum(n//k for k in range(1,isqrt(n)+1))-isqrt(n)**2   
def A001694gen(): return filter(lambda n: n == 1 or min(factorint(n).values()) > 1, count(1))     
def A019565(n): return prod(prime(i+1) for i,v in enumerate(bin(n)[:1:-1]) if v == '1') if n > 0 else 1
def A006882(n): return factorial2(n)
if sys.version_info >= (3,10):
    def A005187(n): return 2*n-n.bit_count()
else:
    def A005187(n): return 2*n-bin(n).count('1')
def A001003gen(): # generator of terms
    m, k = 1, 1
    yield m
    yield k
    for n in count(3):
        m, k = k, (k*(6*n-9)-(n-3)*m)//n
        yield k
def A005836(n): return int(format(n-1,'b'),3)
def A002496gen(): return filter(isprime, (n+1 for n in accumulate(count(0),lambda x,y:x+2*y-1)))
def A052382gen(): return filter(lambda n:'0' not in str(n),count(1))
def A003714(n):
    tlist, s = [1,2], 0
    while tlist[-1]+tlist[-2] <= n:
        tlist.append(tlist[-1]+tlist[-2])
    for d in tlist[::-1]:
        s *= 2
        if d <= n:
            s += 1
            n -= d
    return s
def A026741(n): return n if n % 2 else n//2
def A006567gen(): return filter(lambda p: str(p) != str(p)[::-1] and isprime(int(str(p)[::-1])), (prime(n) for n in count(1)))
def A006370(n):
    q, r = divmod(n, 2)
    return 3*n+1 if r else q
def A151800(n): return nextprime(n)
def A051903(n): return max(factorint(n).values()) if n > 1 else 0
def A001850gen(): # generator of terms
    m, k = 1, 3
    yield m
    yield k
    for n in count(2):
        m, k = k, (k*(6*n-3)-(n-1)*m)//n
        yield k
def A002293(n): return comb(4*n,n)//(3*n+1)
def A002293gen(): # generator of terms
    m = 1
    yield m
    for n in count(0):
        m = m*4*(4*n+3)*(4*n+2)*(4*n+1)//((3*n+2)*(3*n+3)*(3*n+4))
        yield m
def A098550gen(): # generator of terms
    yield 1
    yield 2
    yield 3
    l1, l2, s, b = 3, 2, 4, set()
    while True:        
        i = s
        while True:
            if not i in b and gcd(i,l1) == 1 and gcd(i,l2) > 1:
                yield i
                l2, l1 = l1, i
                b.add(i)
                while s in b:
                    b.remove(s)
                    s += 1
                break
            i += 1
def A001220gen(): return filter(lambda p:pow(2,p-1,p*p) == 1, (prime(n) for n in count(1)))
def A047999_T(n,k): return int(not ~n & k)
@lru_cache(maxsize=None)
def A001175(n):
    if n == 1:
        return 1
    f = factorint(n)
    if len(f) > 1:
        return lcm(*(A001175(a**f[a]) for a in f))
    else:
        k,x = 1, [1,1]
        while x != [0,1]:
            k += 1
            x = [x[1], (x[0]+x[1]) % n]
        return k
def A066272(n): return len([d for d in divisors(2*n) if n > d >=2 and n%d]) + \
    len([d for d in divisors(2*n-1) if n > d >=2 and n%d]) + \
    len([d for d in divisors(2*n+1) if n > d >=2 and n%d])
@lru_cache(maxsize=None)
def A002321(n):
    if n == 0:
        return 0
    c, j = n, 2
    k1 = n//j
    while k1 > 1:
        j2 = n//k1 + 1
        c += (j2-j)*A002321(k1)
        j, k1 = j2, n//j2
    return j-c

if sys.version_info >= (3,10):
    def A029837(n): return n.bit_length() - (1 if n.bit_count() == 1 else 0)
else:
    def A029837(n): return n.bit_length() - (1 if bin(n).count('1') == 1 else 0)
def A007376gen(): return (int(d) for n in count(0) for d in str(n))
def A054632gen(): return accumulate(A007376gen())
def A127353gen(): return islice(A007376gen(),2,None,2)
def A127050gen(): return islice(A007376gen(),1,None,2)
def A127950gen(): return islice(A007376gen(),2,None,8)
def A347345gen(): return filter(lambda k: set(str(k*(k+1)//2)) <= {'1','3','5','7','9'}, (int(''.join(d)) for l in count(1) for d in product('13579',repeat=l)))
def A132739(n): 
    a, b = divmod(n, 5)
    while b == 0:
        a, b = divmod(a,5)
    return 5*a+b
def A349487(n): 
    a, b = divmod(n*n-25, 5)
    while b == 0:
        a, b = divmod(a,5)
    return 5*a+b
def A349791(n):
    b = primepi(n**2)+primepi((n+1)**2)+1
    return (prime(b//2)+prime((b+1)//2))//2 if b % 2 else prime(b//2)
def A000188(n): return isqrt(n//core(n))
def A020449gen(): return filter(isprime,(int(format(n,'b')) for n in count(1)))
def A033676(n):
    d = divisors(n)
    return d[(len(d)-1)//2]
def A047994(n): return prod(p**e-1 for p, e in factorint(n).items())
def d(n,m): return not n % m
def A007678(n): return (1176*d(n,12)*n - 3744*d(n,120)*n + 1536*d(n,18)*n - d(n,2)*(5*n**3 - 42*n**2 + 40*n + 48) - 2304*d(n,210)*n + 912*d(n,24)*n - 1728*d(n,30)*n - 36*d(n,4)*n - 2400*d(n,42)*n - 4*d(n,6)*n*(53*n - 310) - 9120*d(n,60)*n - 3744*d(n,84)*n - 2304*d(n,90)*n + 2*n**4 - 12*n**3 + 46*n**2 - 84*n)//48 + 1
def A063990gen(): return filter(lambda n: divisor_sigma(n)-2*n and not divisor_sigma(divisor_sigma(n)-n)-divisor_sigma(n),count(2))
def A051674(n): return prime(n)**prime(n)
def A001951(n): return isqrt(2*n**2)
def A000587gen(): # generator of terms
    yield 1
    yield -1
    blist, b = [1], -1
    while True:
        blist = list(accumulate([b]+blist))
        b = -blist[-1]
        yield b
def A003132(n): return sum(int(d)**2 for d in str(n))
def A003601gen(): return filter(lambda n:not sum(divisors(n)) % divisor_count(n),count(1))
@lru_cache(maxsize=None)
def A002088(n): # based on second formula in A018805
    if n == 0:
        return 0
    c, j = 0, 2
    k1 = n//j
    while k1 > 1:
        j2 = n//k1 + 1
        c += (j2-j)*(2*A002088(k1)-1)
        j, k1 = j2, n//j2
    return (n*(n-1)-c+j)//2
def A045917(n): return sum(1 for i in range(2,n+1) if isprime(i) and isprime(2*n-i))
def A019546gen(): return filter(lambda n: set(str(n)) <= {'2','3','5','7'},(prime(n) for n in count(1)))
def A011540gen(): return filter(lambda n: '0' in str(n), count(0))
def A014963(n):
    y = factorint(n)
    return list(y.keys())[0] if len(y) == 1 else 1        
def A115004(n): return n**2 + sum(totient(i)*(n+1-i)*(2*n+2-i) for i in range(2,n+1))          
def A316524(n):
    fs = [primepi(p) for p in factorint(n,multiple=True)]
    return sum(fs[::2])-sum(fs[1::2])
def A048050(n): return 0 if n == 1 else divisor_sigma(n)-n-1
def A349806(n):
    for i in count(n**2+(n%2)+1,2):
        fs = factorint(i)
        if len(fs) == 2 == sum(fs.values()):
            return i-n**2
def A099610(n):
    for i in count(n**2+(n%2)+1,2):
        fs = factorint(i)
        if len(fs) == 2 == sum(fs.values()):
            return i
def A348762(n): 
    a, b = divmod(n*n-64, 2)
    while b == 0:
        a, b = divmod(a,2)
    return 2*a+b
def A069834(n): 
    a, b = divmod(n*n+n, 2)
    while b == 0:
        a, b = divmod(a,2)
    return 2*a+b
def A328447(n):
    if n == 0: return 0
    s = str(n)
    l, s = len(s), ''.join(sorted(s.replace('0','')))
    return int(s[0]+'0'*(l-len(s))+s[1:])
def A005188gen(): # generator of terms
    for k in range(1,40):
        a = [i**k for i in range(10)]
        yield from (x[0] for x in sorted(filter(lambda x:x[0] > 0 and tuple(int(d) for d in sorted(str(x[0]))) == x[1], \
                          ((sum(map(lambda y:a[y],b)),b) for b in combinations_with_replacement(range(10),k)))))
def A031443gen(): # generator of terms
    for n in count(1):
        yield from (int('1'+''.join(p),2) for p in multiset_permutations('0'*n+'1'*(n-1)))
def A071925gen(): # generator of terms
    for n in count(1):
        yield from (int('1'+''.join(p)) for p in multiset_permutations('0'*n+'1'*(n-1)))
def A349929gen(): # generator of terms
    for n in count(3,3):
        if 3*gcd(comb(n*(n*(n + 6) - 6) + 2,6*n*(n-1)+3),n**3) == n**3:
            yield n
def A349509(n): return n**3//gcd(comb(n*(n*(n + 6) - 6) + 2,6*n*(n-1)+3),n**3)
def A099611(n):
    for i in count(n**2-(n%2)-1,-2):
        fs = factorint(i)
        if len(fs) == 2 == sum(fs.values()):
            return i
def A349809(n):
    for i in count(n**2-(n%2)-1,-2):
        fs = factorint(i)
        if len(fs) == 2 == sum(fs.values()):
            return n**2-i        
def A002982gen(): return filter(lambda n: isprime(factorial(n)-1),count(1))
def A000058gen(): # generator of terms
    yield (a := 2)
    while True:
        a = a*(a-1)+1
        yield a
def A151799(n): return prevprime(n)
def A000078gen(): # generator of terms
    b = [0, 0, 0, 1]
    yield from b
    while True:
        yield (c := sum(b))
        b = b[1:]+[c]
def A002054(n): return comb(2*n+1,n-1)
def A006720gen(): # generator of terms
    b = [1,1,1,1]
    yield from b
    while True:
        yield (c := (b[-1]*b[-3]+b[-2]**2)//b[-4])
        b = b[1:]+[c]
def A033677(n): return (lambda d:d[len(d)//2])(divisors(n))
def A078972gen(): #generator of terms
    for n in count(0):
        yield from sorted(prod(p) for p in combinations_with_replacement(sieve.primerange(10**n,10**(n+1)),2))
def A005493gen(): #generator of terms
    blist, b = [1], 1
    while True:
        blist = list(accumulate([b]+blist))
        b = blist[-1]    
        yield blist[-2]
def A188014(n): return int((isqrt(5*n**2)+n)//2 -(isqrt(5*(n-4)**2)+n)//2 - 4) if n > 3 else 1-(n % 2)
def A348209(n):
    if n > 2 and bin(n).count('1') == 1: return 0
    k, m, n1, n2, n3 = 1, 2, n**(n-2), n**(n-1), n**n 
    while m < n2:
        k += 1
        m = (2*m) % n3
    while k <= n3:
        if m >= n1:
            a = ispandigital0(m,n)
            if a[0] and ((not a[1]) or m >= n2): return k
        k += 1
        m = (2*m) % n3
    return 0
def A000978gen(): return filter(lambda p: isprime((2**p+1)//3), (prime(n) for n in count(2)))
def A007500gen(): return filter(lambda p: isprime(int(str(p)[::-1])), (prime(n) for n in count(1)))
def A010784gen(): return filter(lambda n: len(set(str(n))) == len(str(n)), count(0))
def A050278gen(): return (int(e+''.join(d)) for e in '123456789' for d in permutations('0123456789'.replace(e,''),9))
def A071924(n): return primepi(max(primefactors(next(islice((int(e+''.join(d)) for e in '123456789' for d in permutations('0123456789'.replace(e,''),9)),n-1,None)))))
def A071924gen(): return (primepi(max(primefactors(m))) for m in (int(e+''.join(d)) for e in '123456789' for d in permutations('0123456789'.replace(e,''),9)))
def A000538(n): return n*(n**2*(n*(6*n + 15) + 10) - 1)//30
def A330151(n): return 8*n*(n**2*(n*(6*n + 15) + 10) - 1)//15
def A259317(n): return n*(n*(n**2*(n*(16*n + 48) + 40) - 11) - 3)//45
def A254640(n): return n*(n*(n*(n*(n*(n*(n*(n*(10*n + 135) + 720) + 1890) + 2394) + 945) - 640) - 450) + 36)//5040
def A002109gen(): return accumulate((k**k for k in count(0)),mul)
def A002109(n): return prod(k**k for k in range(1,n+1))
@lru_cache(maxsize=None)
def A018805(n): # based on second formula in A018805
    if n == 0:
        return 0
    c, j = 1, 2
    k1 = n//j
    while k1 > 1:
        j2 = n//k1 + 1
        c += (j2-j)*A018805(k1)
        j, k1 = j2, n//j2
    return n*(n-1)-c+j
def A023194gen(): # generator of terms
    yield 2
    yield from filter(lambda n:isprime(divisor_sigma(n)),(n**2 for n in count(1)))
def A010057(n): return int(integer_nthroot(n,3)[1])
def A001286(n): return (n-1)*factorial(n)//2
def A001286gen(): # generator of terms
    b = 1
    yield b
    for n in count(2):
        b = b*n*(n+1)//(n-1)
        yield b
def A007602gen(): return filter(lambda n: not ('0' in str(n) or n % prod(int(d) for d in str(n))), count(1))
def A001608gen(): # generator of terms
    a, b, c = 3, 0, 2
    yield from (a,b,c)
    while True:
        a, b, c = b, c, a+b
        yield c
def A031971(n): return harmonic(n,-n)
def A348470(n): return 1 if n == 1 else min(primefactors(next(islice(A064413gen(),n-1,None))))
def A348470gen(): yield from (min(primefactors(n)) if n > 1 else 1 for n in A064413gen())
def A349662(n): return 0 if n <= 1 else isqrt(n**3-1) - n
def A349993(n): return isqrt(n**3) - n + 1
def A349792gen(): # generator of terms
    p1 = 0
    for n in count(1):
        p2 = primepi((n+1)**2)
        b = p1 + p2 + 1
        if b % 2:
            p = prime(b//2)
            q = nextprime(p)
            if p+q == 2*n*(n+1):
                yield n
        p1 = p2
def A308533gen(): # generator of terms
    for n in count(3):
        a = antidivisors(n)
        if int(''.join(str(s) for s in a)) % sum(a) == 0:
            yield n
def A130846(n): return int(''.join(str(s) for s in antidivisors(n)))
def A003278(n): return int(format(n-1,'b'),3)+1 
def A000539(n): return n**2*(n**2*(n*(2*n + 6) + 5) - 1)//12
def A027868gen():
    yield from [0]*5
    p5 = 0
    for n in count(5,5):
        p5 += multiplicity(5, n)
        yield from [p5]*5
def A187950(n): return int((isqrt(5*(n+4)**2)+n)//2 -(isqrt(5*n**2)+n)//2 - 4)
def A018900gen(): return (2**a+2**b for a in count(1) for b in range(a))
@lru_cache(maxsize=None)
def A005728(n): # based on second formula in A018805
    if n == 0:
        return 1
    c, j = -2, 2
    k1 = n//j
    while k1 > 1:
        j2 = n//k1 + 1
        c += (j2-j)*(2*A005728(k1)-3)
        j, k1 = j2, n//j2
    return (n*(n-1)-c+j)//2
def A007629gen(): #generator of terms
    for n in count(10):
        x = [int(d) for d in str(n)]
        y = sum(x)
        while y < n:
            x, y = x[1:]+[y], 2*y-x[0]
        if y == n:     
            yield n
def A007774gen(): return filter(lambda n: len(primefactors(n))==2,count(1))
def A009994gen(): #generator of terms
    yield 0
    yield from (int(''.join(i)) for l in count(1) for i in combinations_with_replacement('123456789',l))
def A004159(n): return sum(int(d) for d in str(n*n))        
def A001952(n): return 2*n+isqrt(2*n**2)
def A005917(n): return n*(n*(4*n - 6) + 4) - 1
def A031347(n):
    while n > 9:
       n = prod(int(d) for d in str(n))
    return n
def A069010(n): return sum(1 for d in bin(n)[2:].split('0') if len(d))
def A005823(n): return 2*int(format(n-1,'b'),3)
def A014311gen(): return (2**a+2**b+2**c for a in count(2) for b in range(1,a) for c in range(b))
def A349783(n): return sum(abs(stirling(2*n,j,kind=1)) for j in range(n+1))
def A011971gen(): # generator of terms
    blist = [1]
    yield 1
    while True:
        b = blist[-1]
        blist = list(accumulate([b]+blist))
        yield from blist
def A046936gen(): # generator of terms
    yield 0        
    blist = [1,1]
    yield from blist
    while True:
        b = blist[-1]
        blist = list(accumulate([b]+blist))
        yield from blist
def A349960(n):
    if n <= 2:
        return 3-n
    a, b = '', ''
    for i in count(1,2):
        a += str(i)
        b += str(i+1)
        ai, bi = int(a), int(b)
        if len(a)+n-2 == len(b): return bi//ai
        m = 10**(n-2-len(b)+len(a))
        lb = bi*m//(ai+1)
        ub = (bi+1)*m//ai
        if lb == ub: return lb
def A349958(n): 
    for j in range(n+1):
        for k in range(j+1):
            if comb(j,k) % n == 0: return j
def A045918(n): return int(''.join([str(len(m.group(0)))+m.group(0)[0] for m in finditer(r'(\d)\1*',str(n))]))
def A001602(n):
    a, b, i, p = 0, 1, 1, prime(n)
    while b % p:
        a, b, i = b, (a+b) % p, i+1
    return i
def A014577(n):
    s = bin(n+1)[2:]
    m = len(s)
    i = s[::-1].find('1')
    return 1-int(s[m-i-2]) if m-i-2 >= 0 else 1
def A081145gen(): # generator of terms
    yield from [1,2]
    l, s, b1, b2 = 2, 3, set(), set([1])
    for n in count(3):
        i = s
        while True:
            m = abs(i-l)
            if not (i in b1 or m in b2):
                yield i
                b1.add(i)
                b2.add(m)
                l = i
                while s in b1:
                    b1.remove(s)
                    s += 1
                break
            i += 1
def A000127(n): return n*(n*(n*(n - 6) + 23) - 18)//24 + 1
def A007407(n): return sum(Fraction(1,k**2) for k in range(1,n+1)).denominator
def A039724(n):
    s, q = '', n
    while q >= 2 or q < 0:
        q, r = divmod(q, -2)
        if r < 0:
            q += 1
            r += 2
        s += str(r)
    return int(str(q)+s[::-1])
def A065855(n): return 0 if n < 4 else n - primepi(n) - 1
def A004290(n):
    if n > 0:
        for i in range(1,2**n):
            x = int(bin(i)[2:])
            if not x % n:
                return x
    return 0
def A006521gen(): return filter(lambda n:pow(2,n,n)==n-1, count(1))
def A124240gen(): return filter(lambda n:n % reduced_totient(n) == 0,count(1))
def A289257gen(): return filter(lambda n:2*n % reduced_totient(2*n) == 0 and pow(2,n,n)==n-1, count(1))
def A306302(n): return 2*n*(n+1) + sum(totient(i)*(n+1-i)*(2*n+2-i) for i in range(2,n+1))
def A307720gen(): # generator of terms. Greedy algorithm
    yield 1
    c, b = Counter(), 1
    while True:
        k, kb = 1, b
        while c[kb] >= kb:
            k += 1
            kb += b
        c[kb] += 1
        b = k
        yield k
def A007569(n): return 2 if n == 2 else n*(42*(not n % 12) - 144*(not n % 120) + 60*(not n % 18) - 96*(not n % 210) + 35*(not n % 24)- 38*(not n % 30) - 82*(not n % 42) - 330*(not n % 60) - 144*(not n % 84) - 96*(not n % 90)) + (n**4 - 6*n**3 + 11*n**2 + 18*n -(not n % 2)*(5*n**3 - 45*n**2 + 70*n - 24) - 36*(not n % 4)*n - 4*(not n % 6)*n*(45*n - 262))//24
def A003401gen(): return filter(lambda n:format(totient(n),'b').count('1') == 1,count(1))
def A014127gen(): return filter(lambda p:pow(3,p-1,p*p) == 1, (prime(n) for n in count(1)))
def A031346(n):
    mp = 0
    while n > 9:
        n = prod(int(d) for d in str(n))
        mp += 1
    return mp
def A029967gen(): return filter(lambda n:palQ(n,12),palQgen10())
def A029968gen(): return filter(lambda n:palQ(n,13),palQgen10())
def A049445gen(): return filter(lambda n:not n % sum([int(d) for d in bin(n)[2:]]), count(1))
def A348623gen(): # generator of terms
    n = 1
    yield n
    while True:
        n = prod(q+1 for p, q in factorint(n).items() if p > 2)
        yield n
def A349775sumsetgen(n): # generate sums of 2 subsets A,B with |A|,|B| >= 2 for A349775 
    for l in range(2,n+2):
        for a in combinations(range(n+1),l):
            amax = max(a)
            bmax = min(amax,n-amax)
            for lb in range(2,bmax+2):
                for b in combinations(range(bmax+1),lb):
                    yield tuple(sorted(set(x+y for x in a for y in b)))     
def A349775(n):
    c = Counter()
    for s in set(A349775sumsetgen(n)):
        c[len(s)] += 1
    for i in range(n+1,1,-1):
        if c[i] < comb(n+1,i):
            return i
def A002779gen(): return filter(lambda n: str(n)==str(n)[::-1],(n**2 for n in count(0)))
def A004185(n): return int(''.join(sorted(str(n))).replace('0','')) if n > 0 else 0
def A029731gen(): return filter(lambda n:palQ(n,16),palQgen10())
def A029804gen(): return filter(lambda n:palQ(n,8),palQgen10())
def A037861(n): return 2*format(n,'b').count('0')-len(format(n,'b'))
def A056608(n): return min(factorint(composite(n)))
def A006261(n): return (n*(n*(n*(n*(n - 5) + 25) + 5) + 94) + 120)//120
def A006561(n): return 0 if n == 2 else n*(42*(not n % 12) - 144*(not n % 120) + 60*(not n % 18) - 96*(not n % 210) + 35*(not n % 24)- 38*(not n % 30) - 82*(not n % 42) - 330*(not n % 60) - 144*(not n % 84) - 96*(not n % 90)) + (n**4 - 6*n**3 + 11*n**2 - 6*n -(not n % 2)*(5*n**3 - 45*n**2 + 70*n - 24) - 36*(not n % 4)*n - 4*(not n % 6)*n*(45*n - 262))//24
def A001129gen(): # generator of terms
    r1, r2 = 1, 0
    yield r2
    yield r1
    while True:
        l, r2 = r1+r2, r1
        r1 = int(str(l)[::-1])
        yield l
def A034838gen(): # generator of terms
    for g in count(1):
        for n in product('123456789',repeat=g):
            s = ''.join(n)
            m = int(s)
            if not any(m % int(d) for d in s):
                yield m  
def A076479(n): return mobius(prod(primefactors(n)))
def A229037gen(): # generator of terms
    blist = []
    for n in count(0):
        i, j, b = 1, 1, set()
        while n-2*i >= 0:
            b.add(2*blist[n-i]-blist[n-2*i])
            i += 1
            while j in b:
                b.remove(j)
                j += 1
        blist.append(j)
        yield j
def A034709gen(): return filter(lambda n: n % 10 and not n % (n % 10), count(1))
def A051802(n):
    if n == 0:
        return 1
    while n > 9:
        n = prod(int(d) for d in str(n) if d != '0')
    return n
def A054977(n): return 1 if n else 2
def A084937gen(): # generator of terms
    yield from [1,2]
    l1, l2, s, b = 2, 1, 3, set()
    while True:
        i = s
        while True:
            if not i in b and gcd(i,l1) == 1 and gcd(i,l2) == 1:
                yield i
                l2, l1 = l1, i
                b.add(i)
                while s in b:
                    b.remove(s)
                    s += 1
                break
            i += 1
def A099165gen(): return filter(lambda n:palQ(n,32),palQgen10())
def A133500(n):
    s = str(n)
    l = len(s)
    m = int(s[-1]) if l % 2 else 1
    for i in range(0,l-1,2):
        m *= int(s[i])**int(s[i+1])
    return m
def A023109(n):
    if n > 0:
        k = 0
        while True:
            m = k
            for i in range(n):
                if str(m) == str(m)[::-1]:
                    break
                m += int(str(m)[::-1])
            else:
                if str(m) == str(m)[::-1]:
                    return k
            k += 1
    else:
        return 0
def A023330gen(): return filter(lambda p:all((isprime(2**m*(p+1)-1) for m in range(1,6))),(prime(n) for n in count(1)))
def A071321(n):
    fs = factorint(n,multiple=True)
    return sum(fs[::2])-sum(fs[1::2])
def A290447(n):
    p,p2 = set(), set()
    for b,c,d in combinations(range(1,n),3):
        e = b + d - c
        f1, f2, g = Fraction(b*d,e), Fraction(b*d*(c-b)*(d-c),e**2), (n-1)*e - 2*b*d
        for i in range(n-d):
            if 2*i*e < g:
                p2.add((i+f1, f2))
            elif 2*i*e == g:
                p.add(f2)
            else:
                break
    return len(p)+2*len(p2)
def A000387gen(): # generator of terms
    m, x = 1, 0
    for n in count(0):
        x, m = x*n + m*(n*(n-1)//2), -m
        yield x
def A003893gen(): # generator of terms
    a, b, = 0, 1
    yield a
    while True:
        a, b = b, (a+b) % 10 
        yield a
def A051801(n): return prod(int(d) for d in str(n) if d != '0') if n > 0 else 1    
def A001917(n):
    p = prime(n)
    return 1 if n == 2 else (p-1)//n_order(2,p)
def A007540gen(): # generator of terms
    for n in count(1):
        p, m = prime(n), 1
        p2 = p*p
        for i in range(2,p):
            m = (m*i) % p2
        if m == p2-1:
            yield p
def A027870(n): return str(2**n).count('0')
def A029955gen(): return palQgen(9)
def A061910gen(): return filter(lambda n:is_square(sum(int(d) for d in str(n*n))),count(1))
def A006721gen(): # generator of terms
    blist = [1,1,1,1,1]
    yield from blist
    for n in count(5):
        blist = blist[1:]+[(blist[-1]*blist[-4]+blist[-2]*blist[-3])//blist[-5]]
        yield blist[-1]
def A087062_T(n,k): return lunar_mul(n,k)
def A007488gen(): return filter(lambda p:is_square(int(str(p)[::-1])),(prime(n) for n in count(1)))
def A059758gen(): # generator of terms
    for l in count(1):
        for a in '1379':
            for b in '0123456789':
                if a != b and isprime(p := int((a+b)*l+a)):
                    yield p
def A175046(n): return int(''.join(d+'1' if '1' in d else d+'0' for d in split('(0+)|(1+)',bin(n)[2:]) if d != '' and d != None),2)
def A228407gen(): # generator of terms
    yield from [0,11]
    l, s, b = Counter('11'), 1, {11}
    while True:
        i = s
        while True:
            if i not in b:
                li, o = Counter(str(i)), 0
                for d in (l+li).values():
                    if d % 2:
                        if o > 0:
                            break
                        o += 1
                else:
                    yield i
                    l = li
                    b.add(i)
                    while s in b:
                        b.remove(s)
                        s += 1
                    break
            i += 1
def A317081(n):
    if n == 0:
        return 1
    c = 0
    for d in partitions(n):
        s = set(d.values())
        if len(s) == max(s):
            c += 1
    return c
def A000979gen(): return filter(isprime,((2**prime(n)+1)//3 for n in count(2)))
def A004094(n): return int(str(2**n)[::-1])
def A029954gen(): return palQgen(7)
def A036691(n): return factorial(composite(n))//primorial(primepi(composite(n))) if n > 0 else 1
def A054377gen(): return filter(lambda n:sum(n/p for p in primefactors(n)) + 1 == n, count(2))
def A227349(n): return prod(len(d) for d in split('0+',bin(n)[2:]) if d) if n > 0 else 1
def A000540(n): return n*(n**2*(n**2*(n*(6*n + 21) + 21) - 7) + 1)//42
def A034947(n):
    s = bin(n)[2:]
    m = len(s)
    i = s[::-1].find('1')
    return 1-2*int(s[m-i-2]) if m-i-2 >= 0 else 1
def A049060(n): return prod((p**(e+1)-2*p+1)//(p-1) for p,e in factorint(n).items())
def A057890gen(): return filter(lambda n:bin(n)[2:].rstrip('0') == bin(n)[2:].rstrip('0')[::-1],count(0))
@lru_cache(maxsize=None)
def A015614(n): # based on second formula in A018805
    if n == 0:
        return -1
    c, j = 2, 2
    k1 = n//j
    while k1 > 1:
        j2 = n//k1 + 1
        c += (j2-j)*(2*A015614(k1)+1)
        j, k1 = j2, n//j2
    return (n*(n-1)-c+j)//2
def A045875(n):
    l, x = [str(d)*n for d in range(10)], 1
    for m in count(0):
        s = str(x)
        for k in l:
            if k in s:
                return m
        x *= 2
def A080670(n): return 1 if n == 1 else int(''.join([str(y) for x in sorted(factorint(n).items()) for y in x if y != 1]))
def A006590(n): return (lambda m: n+2*sum((n-1)//k for k in range(1, m+1))-m*m)(isqrt(n-1))
def A006794gen(): # generator of terms
    p, q = 2, 2
    while True:
        if isprime(q-1):
            yield p
        p = nextprime(p)
        q *= p
def A036229(n):
    k, r, m = (10**n-1)//9, 2**n-1, 0
    while m <= r:
        t = k+int(bin(m)[2:])
        if isprime(t):
            return t
        m += 1
    return -1
def A047842(n):
    s, x = '', str(n)
    for i in range(10):
        y = str(i)
        c = str(x.count(y))
        if c != '0':
            s += c+y
    return int(s)
def A233466gen(): return filter(lambda n:2*totient(n) == n-5,count(1,2))
def A078971gen(): # generator of terms
    for t in count(0):
        yield (2**(2*t)-1)//3
        yield from ((2**(2*t+1)+2**(2*j+1)-1)//3 for j in range(t))
def A048054(n): return len([p for p in primerange(10**(n-1),10**n) if isprime(int(str(p)[::-1]))])
def A059729(n):
    s = [int(d) for d in str(n)]
    l = len(s)
    t = [0]*(2*l-1)
    for i in range(l):
        for j in range(l):
            t[i+j] = (t[i+j] + s[i]*s[j]) % 10
    return int("".join(str(d) for d in t))
if sys.version_info >= (3,10):
    def A159918(n): return n*n.bit_count()
else:
    def A159918(n): return bin(n*n).count('1')
def A061712(n):
    l, k = n-1, 2**n
    while True:
        for d in combinations(range(l-1,-1,-1),l-n+1):
            m = k-1 - sum(2**(e) for e in d)
            if isprime(m):
                return m
        l += 1
        k *= 2
def A106737(n): return sum(int(not (~(n+k) & (n-k)) | (~n & k)) for k in range(n+1))
def A110566(n): return lcm([k for k in range(1,n+1)])//harmonic(n).q
def A256630gen(): # generator of terms
    for l in count(0):
        for a in ('1','2','3','4'):
            for b in product('01234',repeat = l):
                for c in ('0','1','2'):
                    s = a+''.join(b)+c
                    if '0' in s and '4' in s:
                        n = int(s)
                        s2 = set(str(n**2))
                        if {'0','4'} <= s2 <= {'0','1','2','3','4'}:
                            yield n
def A007608(n):
    s, q = '', n
    while q >= 4 or q < 0:
        q, r = divmod(q, -4)
        if r < 0:
            q += 1
            r += 4
        s += str(r)
    return int(str(q)+s[::-1])                            
def A000139gen(): # generator of terms
    b = 2
    yield b
    for n in count(1):
        b = 3*(3*n-2)*(3*n-1)*b//(2*n+2)//(2*n+1)
        yield b
def A000139(n): return 2 if n==0 else 2*comb(3*n, n-1)//n//(n+1)
def A065197gen(): return filter(lambda n:n==reduce(lambda m, k: m + (k if (m//k) % 2 else -k),range(n,1,-1),n),count(1))
def A014847gen(): # generator of terms
    b = 1
    for n in count(1):
        if not b % n:
            yield n
        b = b*(4*n+2)//(n+2)
def A050486(n): return (2*n+7)*comb(n + 6, 6)//7
def A053347(n): return (n+4)*comb(n + 7, 7)//4
def A057147(n): return n*sum(int(d) for d in str(n))
def A063655(n):
    d = divisors(n)
    l = len(d)
    return d[(l-1)//2] + d[l//2]
def A074832gen(): return filter(lambda p: isprime(int(bin(p)[:1:-1],2)), (prime(n) for n in count(1)))
def A175498gen(): # generator of terms   
    yield from [1,2]
    l, s, b1, b2 = 2, 3, set(), {1}
    for n in count(3):
        i = s
        while True:
            if not (i in b1 or i-l in b2):
                yield i
                b1.add(i)
                b2.add(i-l)
                l = i
                while s in b1:
                    b1.remove(s)
                    s += 1
                break
            i += 1
def A000475gen(): # generator of terms
    m, x = 1, 0
    for n in count(4):
        x, m = x*n + m*comb(n,4), -m
        yield x
def A003684(n): return len([p for p in primerange(10**(n-1),10**n) if len(set(str(p))) == len(str(p)) and isprime(int(str(p)[::-1]))])
def A007497gen(): return accumulate(repeat(2), lambda x, _: divisor_sigma(x))
def A031877gen(): # generator of terms
    for n in count(1):
        if n % 10:
            s1 = str(n)
            s2 = s1[::-1]
            if s1 != s2 and not n % int(s2): yield n
def A038189(n):
    s = bin(n)[2:]
    m = len(s)
    i = s[::-1].find('1')
    return int(s[m-i-2]) if m-i-2 >= 0 else 0
@lru_cache(maxsize=None)
def A071778(n):
    if n == 0:
        return 0
    c, j = 1, 2
    k1 = n//j
    while k1 > 1:
        j2 = n//k1 + 1
        c += (j2-j)*A071778(k1)
        j, k1 = j2, n//j2
    return n*(n**2-1)-c+j
def A078241(n):
    if n > 0:
        for i in range(1,2**n):
            x = 2*int(bin(i)[2:])
            if not x % n:
                return x
    return 0
def A161710(n): return n*(n*(n*(n*(n*(n*(154 - 6*n) - 1533) + 7525) - 18879) + 22561) - 7302)//2520 + 1
def A161713(n): return n*(n*(n*(n*(15 - n) - 65) + 125) - 34)//40 + 1
def A250408gen(): return filter(lambda n:palQ(n,20),palQgen10())
def A345957(n):
    if n == 1:
        return 1
    fs = factorint(n,multiple=True)
    q, r = divmod(len(fs),2)
    return 0 if r else len(list(multiset_combinations(fs,q)))
def A004520(n): return int(''.join(str(2*int(d) % 10) for d in str(n)))
def A005807gen(): # generator of terms
    b = 2
    yield b
    for n in count(0):
        b = b*(4*n+2)*(5*n+9)//((n+3)*(5*n+4)) 
        yield b
def A014707(n):
    s = bin(n+1)[2:]
    m = len(s)
    i = s[::-1].find('1')
    return int(s[m-i-2]) if m-i-2 >= 0 else 0
def A031423gen(): # generator of terms
    for n in count(1):
        cf = continued_fraction_periodic(0,1,n)
        if len(cf) > 1 and len(cf[1]) > 1 and len(cf[1]) % 2 and cf[1][len(cf[1])//2] == 10:
            yield n
def A114043(n): return 4*n**2-6*n+3 + 2*sum(totient(i)*(n-i)*(2*n-i) for i in range(2,n))
def A249156gen(): return filter(lambda n:palQ(n,7),palQgen(5))
def A250410gen(): return filter(lambda n:palQ(n,25),palQgen10())
def A000449gen(): # generator of terms
    m, x = 1, 0
    for n in count(3):
        x, m = x*n + m*(n*(n-1)*(n-2)//6), -m
        yield x
def A000541(n): return n**2*(n**2*(n**2*(n*(3*n + 12) + 14) - 7) + 2)//24
def A001287(n): return comb(n,10)
def A022842(n): return isqrt(8*n**2)
def A031286(n):
    ap = 0
    while n > 9:
        n = sum(int(d) for d in str(n))
        ap += 1
    return ap
def A055165(n): return sum(1 for s in product([0,1],repeat=n**2) if Matrix(n,n,s).det() != 0)
def A145768(n): return reduce(xor, (x**2 for x in range(n+1)))
def A145829gen(): # generator of terms
    m = 0
    for n in count(1):
        m ^= n**2
        a, b = integer_nthroot(m,2)
        if b: yield a
def A145828gen(): # generator of terms
    m = 0
    for n in count(0):
        m ^= n**2
        if isqrt(m)**2 == m: yield m
def A193232(n): return reduce(xor, (x*(x+1) for x in range(n+1)))//2
def A062700gen(): # generator of terms
    yield 3
    yield from filter(isprime,(divisor_sigma(d**2) for d in count(1)))
def A065710(n): return str(2**n).count('2')
def A215732(n):
    l, x = [str(d)*n for d in range(10)], 1
    while True:
        s = str(x)
        for k in range(10):
            if l[k] in s:
                return k
        x *= 2
def A260343gen(): return filter(lambda n:isprime(intbase(list(range(1,n))+[1,0]+list(range(n-1,0,-1)), n)),count(2))
def A320486(n): return int('0'+''.join(d if str(n).count(d) == 1 else '' for d in str(n)))
def A002708gen(): # generator of terms
    a, b = 1, 1
    for n in count(1):
        yield a % n
        a, b = b, a+b
def A003098gen(): return filter(lambda m:str(m)==str(m)[::-1],(n*(n+1)//2 for n in range(10**5)))
def A005001gen(): # generator of terms
    yield from [0,1,2]
    blist, a, b = [1], 2, 1
    while True:
        blist = list(accumulate([b]+blist))
        b = blist[-1]
        a += b
        yield a
def A006533(n): return (1176*(not n % 12)*n - 3744*(not n % 120)*n + 1536*(not n % 18)*n - (not n % 2)*(5*n**3 - 42*n**2 + 40*n + 48) - 2304*(not n % 210)*n + 912*(not n % 24)*n - 1728*(not n % 30)*n - 36*(not n % 4)*n - 2400*(not n % 42)*n - 4*(not n % 6)*n*(53*n - 310) - 9120*(not n % 60)*n - 3744*(not n % 84)*n - 2304*(not n % 90)*n + 2*n**4 - 12*n**3 + 46*n**2 - 36*n)//48 + 1
def A018796(n):
    if n == 0:
        return 0
    else:
        d, nd = 1, n
        while True:
            x = (isqrt(nd-1)+1)**2
            if x < nd+d:
                return int(x)
            d *= 10
            nd *= 10
def A027611(n): return (n*harmonic(n)).q
def A037015gen(): # generator of terms
    for n in count(0):
        c = None
        for x, y in groupby(bin(n)[2:]):
            z = len(list(y))
            if c != None and z >= c:
                break
            c = z
        else:
            yield n
def A038003gen(): # generator of terms
    yield from [1,1]
    c, s = 1, 3
    for n in count(2):
        c = (c*(4*n-2))//(n+1)
        if n == s:
            yield c
            s = 2*s+1
def A050782(n):
    if n % 10:
        for i in islice(palQgen10(),1,None):
            q, r = divmod(i, n)
            if not r: return q
    else:
        return 0
def A073327(n): return sum(ord(d)-96 for d in sub("\sand\s|[^a-z]", "", num2words(n)))
def A088177(): # generator of terms
    yield 1
    yield 1
    p, a = {1}, 1
    while True:
        n = 1
        while n*a in p:
            n += 1
        p.add(n*a)
        a = n
        yield n
def A096497(n): return nextprime((10**n-1)//9)
def A101337(n):
    s = str(n)
    l = len(s)
    return sum(int(d)**l for d in s)
def A141255(n): return 2*(n-1)*(2*n-1) + 2*sum(totient(i)*(n-i)*(2*n-i) for i in range(2,n))
def A176774(n):
    k = (isqrt(8*n+1)-1)//2
    while k >= 2:
        a, b = divmod(2*(k*(k-2)+n),k*(k-1))
        if not b:
            return a
        k -= 1
def A002131(n): return prod(p**e if p == 2 else (p**(e+1)-1)//(p-1) for p, e in factorint(n).items())
def A024916(n): return sum(k*(n//k) for k in range(1,n+1))
def A350146(n): return sum(k*(n//k) for k in range(1,n+1))-sum(k*(n//2//k) for k in range(1,n//2+1))
def A252867gen(): # generator of terms
    yield from [0,1,2]
    l1, l2, s, b = 2, 1, 3, set()
    while True:
        i = s
        while True:
            if not (i in b or i & l1) and i & l2:
                yield i
                l2, l1 = l1, i
                b.add(i)
                while s in b:
                    b.remove(s)
                    s += 1
                break
            i += 1 
def A002419(n): return (6*n-2)*comb(n+2,3)//4
def A015950gen(): return filter(lambda n:pow(4,n,n) == n-1,count(1))
def A016069gen(): # generator of terms 
    for g in count(2):
        n, blist = 2**g-1, []
        for x in combinations('0123456789',2):
            for i,y in enumerate(product(x,repeat=g)):
                if i > 0 and i < n and y[0] != '0':
                    z = int(''.join(y))
                    a, b = integer_nthroot(z,2)
                    if b: blist.append(a)
        yield from sorted(blist)
def A350092(n): return floor((1+sqrt(5)/2)**n)
def A014217(n): return floor(((1+sqrt(5))/2)**n)
def A350174gen(): return chain.from_iterable([k]*prime(k+1) for k in count(0))
def A350173(n): return prime(n)**(n%2+1)
def A350171(n): return prime(n)+n%2
def A349425(n):
    if n % 10 == 0: return 0
    m, n1, n2 = n, 10**n, 10**(n-1)
    while (k := pow(n,m,n1)) != m: m = k
    return k//n2
def A309081(n): return n+sum((1 if k%2 else -1)*(n//k**2) for k in range(2,isqrt(n)+1))
def A055882gen(): # generator of terms
    yield from [1,2]
    blist, b, n2 = [1], 1, 4
    while True:
        blist = list(accumulate([b]+blist))
        b = blist[-1]
        yield b*n2
        n2 *= 2
def A068679gen(): # generator of terms
    for n in count(1):
        if isprime(10*n+1):
            s = str(n)
            for i in range(len(s)):
                if not isprime(int(s[:i]+'1'+s[i:])):
                    break
            else:
                yield n
def A082183(n):
    t = n*(n+1)
    ds = divisors(t)
    for i in range(len(ds)//2-2,-1,-1):
        x = ds[i]
        y = t//x
        a, b = divmod(y-x,2)
        if b:
            return a
    return -1
def A098464gen(): # generator of terms
    l, h = 1, Fraction(1, 1)
    for k in count(1):
        l = lcm(l,k)
        h += Fraction(1,k)
        if l == h.denominator:
            yield k
def A109812gen(): # generator of terms
    yield 1
    l1, s, b = 1, 2, set()
    while True:
        i = s
        while True:
            if not (i in b or i & l1):
                yield i
                l1 = i
                b.add(i)
                while s in b:
                    b.remove(s)
                    s += 1
                break
            i += 1
def A132106(n): return (lambda m: 2*(sum(n//k for k in range(1, m+1)))+m*(1-m)+1)(isqrt(n))
def A215727(n):
    l, x = [str(d)*n for d in range(10)], 1
    for m in count(0):
        s = str(x)
        for k in l:
            if k in s:
                return m
        x *= 3
def A000542(n): return n*(n**2*(n**2*(n**2*(n*(10*n + 45) + 60) - 42) + 20) - 3)//90
def A002796gen(): return filter(lambda n: all((d =='0' or n % int(d) == 0) for d in set(str(n))),count(1))
def A004167(n): return int(str(3**n)[::-1])
def A014312gen(): return (2**a+2**b+2**c+2**d for a in count(3) for b in range(2,a) for c in range(1,b) for d in range(c))
def A046732gen(): return filter(lambda p:len(str(p)) == len(set(str(p))) and isprime(int(str(p)[::-1])),(prime(n) for n in count(1)))
def A050985(n): return 1 if n <=1 else reduce(mul,[p**(e % 3) for p,e in factorint(n).items()])
def A061242gen(): return filter(lambda p:not (p+1) % 18,(prime(n) for n in count(1)))
def A061762(n): return sum(a := [int(d) for d in str(n)])+prod(a)
def A219324gen(): # generator of terms
    for n in count(1):
        s = [int(d) for d in str(n)]
        m = len(s)
        if n == Matrix(m, m, lambda i, j: s[(i-j) % m]).det():
            yield n
def A246544gen(): # generator of terms
    for m in count(1):
        n = composite(m)
        x = divisors(n)
        x.pop()
        y = sum(x)
        while y < n:
            x, y = x[1:]+[y], 2*y-x[0]
        if y == n: yield n
def A276037gen(): yield from (int(''.join(d)) for l in count(1) for d in product('15',repeat=l))
def A290131(n): return 2*(n-1)**2 + sum(totient(i)*(n-i)*(2*n-i) for i in range(2,n))
def A317087gen(): # generator of terms
    yield 1
    for n in count(1):
        d = factorint(n)
        k, l = sorted(d.keys()), len(d)
        if l > 0 and l == primepi(max(d)):
            for i in range(l//2):
                if d[k[i]] != d[k[l-i-1]]:
                    break
            else:
                yield n
def A332517(n): return sum(totient(d)*(n//d)**n for d in divisors(n,generator=True))
def A006722gen(): # generator of terms
    blist = [1]*6
    yield from blist
    while True:
        blist = blist[1:]+[(blist[-1]*blist[-5]+blist[-2]*blist[-4]+blist[-3]**2)//blist[-6]]
        yield blist[-1]
def A008863(n): return n*(n*(n*(n*(n*(n*(n*(n*(n*(n - 35) + 600) - 5790) + 36813) - 140595) + 408050) - 382060) + 1368936) + 2342880)//3628800 + 1
def A011965gen(): # generator of terms
    yield 1
    blist = [1, 2]
    while True:
        blist = list(accumulate([blist[-1]]+blist))
        yield blist[-3]
def A034302gen(): # generator of terms
    yield from [23, 37, 53, 73]
    for l in count(1): 
        for d in product('123456789',repeat=l):
            for e in product('1379',repeat=2):
                s = ''.join(d+e)
                if isprime(int(s)):
                    for i in range(len(s)):
                        if not isprime(int(s[:i]+s[i+1:])):
                            break
                    else:
                        yield int(s)
def A036953gen(): return filter(isprime, (int(gmpy2digits(n, 3)) for n in count(0)))
def A054683gen(): return filter(lambda i:not sum(int(d) for d in str(i)) % 2,count(0))
def A064538(n):
    p, m = 2, n+1
    while p <= (n+2)//(2+ (n% 2)):
        if sum(d for d in sympydigits(n+1,p)[1:]) >= p:
            m *= p
        p = nextprime(p)
    return m
def A066321(n):
    if n == 0:
        return 0
    else:
        s, q = '', n
        while q:
            q, r = c_divmod(q, -4)
            s += ('0000','1000','0011','1011')[r]
        return int(s[::-1],2)
@lru_cache(maxsize=None)
def A082540(n):
    if n == 0:
        return 0
    c, j = 1, 2
    k1 = n//j
    while k1 > 1:
        j2 = n//k1 + 1
        c += (j2-j)*A082540(k1)
        j, k1 = j2, n//j2
    return n*(n**3-1)-c+j
def A087116(n): return sum(1 for d in bin(n)[2:].split('1') if len(d))
def A096825(n):
    fs = factorint(n)
    return len(list(multiset_combinations(fs,sum(fs.values())//2)))
@lru_cache(maxsize=None)
def A100448(n):
    if n == 0:
        return 0
    c, j = 2, 2
    k1 = n//j
    while k1 > 1:
        j2 = n//k1 + 1
        c += (j2-j)*(6*A100448(k1)+1)
        j, k1 = j2, n//j2
    return (n*(n**2-1)-c+j)//6
def A129135gen(): # generator of terms
    m, x = 1, 0
    for n in count(5):
        x, m = x*n + m*comb(n,5), -m
        yield x
def A187795(n): return sum(d for d in divisors(n,generator=True) if divisor_sigma(d) > 2*d)
def A246660(n): return prod(factorial(len(d)) for d in split('0+',bin(n)[2:]) if d) if n > 0 else 1
def A256617gen(): return filter(lambda n:len(plist:= primefactors(n))==2 and plist[1]==nextprime(plist[0]),count(1))
def A272369gen(): return filter(lambda n:all((d in (1,2,4,46) or not isprime(d+1)) for d in divisors(n,generator=True)),count(92,92))
def A317086(n):
    if n > 3 and isprime(n):
        return 1
    else:
        c = 1
        for d in partitions(n,k=integer_nthroot(2*n,2)[0],m=n*2//3):
            l = len(d)
            if l > 0:
                k = max(d)
                if l == k:
                    for i in range(k//2):
                        if d[i+1] != d[k-i]:
                            break
                    else:
                        c += 1
        return c
def A331757(n): return 8 if n == 1 else 2*(n*(n+3) + sum(totient(i)*(n+1-i)*(n+1+i) for i in range(2,n//2+1)) + sum(totient(i)*(n+1-i)*(2*n+2-i) for i in range(n//2+1,n+1)))
def A005351(n):
    s, q = '', n
    while q >= 2 or q < 0:
        q, r = divmod(q, -2)
        if r < 0:
            q += 1
            r += 2
        s += str(r)
    return int(str(q)+s[::-1],2)
def A028909(n): return int(''.join(sorted(str(2**n))))
def A028910(n): return int(''.join(sorted(str(2**n),reverse=True)))
def A039723(n):
    s, q = '', n
    while q >= 10 or q < 0:
        q, r = divmod(q, -10)
        if r < 0:
            q += 1
            r += 10
        s += str(r)
    return int(str(q)+s[::-1])
def A055685gen(): return filter(lambda n:pow(2,n,n-1) == n-2,count(2))
def A065712(n): return str(2**n).count('1')
def A067388gen(): # generator of terms
    p = 2
    q, r, s = p+48, p+96, p+144
    while True:
        np = nextprime(p)
        if np == q and isprime(r) and isprime(s) and nextprime(q) == r and nextprime(r) == s:
            yield p
        p, q, r, s = np, np+48, np+96, np+144
def A075101(n): return (Fraction(2**n)/n).numerator
@lru_cache(maxsize=None)
def A090025(n):
    if n == 0:
        return 0
    c, j = 1, 2
    k1 = n//j
    while k1 > 1:
        j2 = n//k1 + 1
        c += (j2-j)*A090025(k1)
        j, k1 = j2, n//j2
    return (n+1)**3-c+7*(j-n-1)
def A350153gen(): return filter(lambda p:isprime(p),(int(s) for n in count(1) for s in accumulate(str(d) for d in chain(range(1,n+1),range(n-1,0,-1)))))
def A259937(n): return int(''.join(str(d) for d in chain(range(1,n+1),range(n,0,-1))))
def A350233gen(): return filter(lambda n:(m := int(str(n)[::-1])) % 5 and not m % 4,filter(lambda n: n % 4 and not n % 5,count(1)))
def A350232gen(): return filter(lambda n:(m := int(str(n)[::-1])) % 4 and not m % 5,filter(lambda n: n % 5 and not n % 4,count(1)))
def A350228gen():
    yield from (1,0)
    b, bdict = 0, {1:(1,),0:(2,)}
    for n in count(3):
        if len(l := bdict[b]) > 1:
            m = (n-1-l[-2])*b
            if m in bdict:
                bdict[m] = (bdict[m][-1],n)
            else:
                bdict[m] = (n,)
            b = m
        else:
            bdict[1] = (bdict[1][-1],n)
            b = 1
        yield b
def A171918gen(): # generator of terms
    yield 8
    b, bdict = 8, {8:(1,)}
    for n in count(2):
        if len(l := bdict[b]) > 1:
            b = n-1-l[-2]
        else:
            b = 0
        if b in bdict:
            bdict[b] = (bdict[b][-1],n)
        else:
            bdict[b] = (n,)
        yield b
def A171917gen(): # generator of terms
    b, bdict = 7, {7:(1,)}
    for n in count(2):
        yield b
        if len(l := bdict[b]) > 1:
            b = n-1-l[-2]
        else:
            b = 0
        if b in bdict:
            bdict[b] = (bdict[b][-1],n)
        else:
            bdict[b] = (n,)
def A171916gen(): # generator of terms
    b, bdict = 6, {6:(1,)}
    for n in count(2):
        yield b
        if len(l := bdict[b]) > 1:
            b = n-1-l[-2]
        else:
            b = 0
        if b in bdict:
            bdict[b] = (bdict[b][-1],n)
        else:
            bdict[b] = (n,)
def A171915gen(): # generator of terms
    b, bdict = 5, {5:(1,)}
    for n in count(2):
        yield b
        if len(l := bdict[b]) > 1:
            b = n-1-l[-2]
        else:
            b = 0
        if b in bdict:
            bdict[b] = (bdict[b][-1],n)
        else:
            bdict[b] = (n,)
def A171914gen(): # generator of terms
    b, bdict = 4, {4:(1,)}
    for n in count(2):
        yield b
        if len(l := bdict[b]) > 1:
            b = n-1-l[-2]
        else:
            b = 0
        if b in bdict:
            bdict[b] = (bdict[b][-1],n)
        else:
            bdict[b] = (n,)
def A171913gen(): # generator of terms
    b, bdict = 3, {3:(1,)}
    for n in count(2):
        yield b
        if len(l := bdict[b]) > 1:
            b = n-1-l[-2]
        else:
            b = 0
        if b in bdict:
            bdict[b] = (bdict[b][-1],n)
        else:
            bdict[b] = (n,)
def A171912gen(): # generator of terms
    b, bdict = 2, {2:(1,)}
    for n in count(2):
        yield b
        if len(l := bdict[b]) > 1:
            b = n-1-l[-2]
        else:
            b = 0
        if b in bdict:
            bdict[b] = (bdict[b][-1],n)
        else:
            bdict[b] = (n,)
def A171911gen(): # generator of terms
    b, bdict = 1, {1:(1,)}
    for n in count(2):
        yield b
        if len(l := bdict[b]) > 1:
            b = n-1-l[-2]
        else:
            b = 0
        if b in bdict:
            bdict[b] = (bdict[b][-1],n)
        else:
            bdict[b] = (n,)
def A181391gen(): # generator of terms
    b, bdict = 0, {0:(1,)}
    for n in count(2):
        yield b
        if len(l := bdict[b]) > 1:
            b = n-1-l[-2]
            if b in bdict:
                bdict[b] = (bdict[b][-1],n)
            else:
                bdict[b] = (n,)
        else:
            b = 0
            bdict[0] = (bdict[0][-1],n)
def A309363gen(): # generator of terms
    b, bdict = 0, {0:(1,)}
    for n in count(2):
        yield b
        if len(l := bdict[b]) > 1:
            b = n-1-l[-2]
        else:
            b = 2
        if b in bdict:
            bdict[b] = (bdict[b][-1],n)
        else:
            bdict[b] = (n,)
def A092221gen(): return filter(lambda n:not bernoulli(2*n).p % 59,count(0))
def A281502gen(): return filter(lambda n:not bernoulli(2*n).p % 691,count(0))
def A100208gen(): # generator of terms
    xset, a = {1}, 1
    yield a
    while True: 
        a, b = 1, 1+a**2
        while not isprime(b) or a in xset:
            b += 2*a+1
            a += 1
        xset.add(a)
        yield a
def A349731(n): return -1 if n == 0 else -(-n)**n*ff(Fraction(1,n),n)
def A109890gen(): # generator of terms
    yield from [1,2]
    s, y, b = 3, 3, set()
    while True:
        for i in divisors(s,generator=True):
            if i >= y and i not in b:
                yield i
                s += i
                b.add(i)
                while y in b:
                    b.remove(y)
                    y += 1
                break
def A110751gen(): return filter(lambda n:primefactors(n) == primefactors(int(str(n)[::-1])),count(1))
def A112822(n):
    k, l, h = 1, 1, Fraction(1,1)
    while l != h.denominator*(2*n-1):
        k += 1
        l = lcm(l,k)
        h += Fraction(1,k)
    return k
def A115005(n): return (n-1)*(2*n-1) + sum(totient(i)*(n-i)*(2*n-i) for i in range(2,n))
def A115920gen(): return filter(lambda n:sorted(str(divisor_sigma(n))) == sorted(str(n)),count(1))
def A115921gen(): return filter(lambda n:sorted(str(totient(n))) == sorted(str(n)),count(1))
def A153671gen(): # generator of terms
    n, k, q = 101, 100, 0
    for m in count(1):
        r = n % k
        if r > q:
            q = r
            yield m
        n *= 101
        k *= 100
        q *= 100
def A215728(n):
    l, x = [str(d)*n for d in range(10)], 1
    for m in count(0):
        s = str(x)
        for k in l:
            if k in s:
                return m
        x *= 5
def A215729(n):
    l, x = [str(d)*n for d in range(10)], 1
    for m in count(0):
        s = str(x)
        for k in l:
            if k in s:
                return m
        x *= 6
def A215730(n):
    l, x = [str(d)*n for d in range(10)], 1
    for m in count(0):
        s = str(x)
        for k in l:
            if k in s:
                return m
        x *= 7
def A215733(n):
    l, x = [str(d)*n for d in range(10)], 1
    while True:
        s = str(x)
        for k in range(10):
            if l[k] in s:
                return k
        x *= 3
def A260273gen(): # generator of terms
    yield 1
    a = 1
    while True:
        b, s = 1, format(a,'b')
        while format(b,'b') in s:
            b += 1
        a += b
        s = format(a,'b')
        yield a
def A331776(n): return 4 if n == 1 else 20*n*(n-1) + 4*sum(totient(i)*(n+1-i)*(2*n+2-i) for i in range(2,n+1))   
def A003128gen(): # generator of terms
    blist, a, b = [1], 1, 1
    while True:
        blist = list(accumulate([b]+blist))
        c = blist[-1]
        yield (c+a-3*b)//2
        a, b = b, c
def A048701(n): return int((s := bin(n-1)[2:])+s[::-1],2)
def A049479(n): return min(factorint(2**n-1))
def A061040(n): return 9*n**2//gcd(n**2-9,9*n**2)
def A064614(n): return prod((5-p if 2<=p<=3 else p)**e for p,e in factorint(n).items()) if n > 1 else n
def A065715(n): return str(2**n).count('4')
def A065719(n): return str(2**n).count('8')
def A072960gen(): return chain([0],(int(a+''.join(b)) for l in count(0) for a in '3689' for b in product('03689',repeat=l)))
@lru_cache(maxsize=None)
def A100449(n):
    if n == 0:
        return 1
    c, j = 0, 2
    k1 = n//j
    while k1 > 1:
        j2 = n//k1 + 1
        c += (j2-j)*((A100449(k1)-3)//2)
        j, k1 = j2, n//j2
    return 2*(n*(n-1)-c+j)+1
def A127936gen(): return filter(lambda i:isprime(int('01'*i+'1',2)),count(1))
def A171901is_ok(n):
    s = str(n)
    return any(s[i] == s[i - 1] for i in range(1, len(s)))
def A171901gen(): return filter(A171901is_ok,count(0))
def A215731(n):
    l, x = [str(d)*n for d in range(10)], 1
    for m in count(0):
        s = str(x)
        for k in l:
            if k in s:
                return m
        x *= 11  
def A215737(n):
    a, s = 1, tuple(str(i)*n for i in range(10))
    while True:
        a *= 11
        t = str(a)
        for i, x in enumerate(s):
            if x in t:
                return i
def A230625(n): return 1 if n == 1 else int(''.join([bin(y)[2:] for x in sorted(factorint(n).items()) for y in x if y != 1]),2)
def A237600gen(): # generator of terms
    n = 2
    while True:
        s = format(n,'x')
        for i in range(1,len(s)):
            if not is_prime(int(s[:-i],16)):
                break
        else:
            yield n
        n = nextprime(n)
def A252648gen(): # generator of terms
    yield 1
    for m in count(1):
        l, L, dm, xlist, q = 1, 1, [d**m for d in range(10)], [0], 9**m
        while l*q >= L:
            for c in combinations_with_replacement(range(1,10),l):
                n = sum(dm[d] for d in c)
                if sorted(int(d) for d in str(n)) == [0]*(len(str(n))-len(c))+list(c):
                    xlist.append(n)
            l += 1
            L *= 10   
        yield from sorted(xlist)
def A272695(n): return int((n*sin(n)).round())
def A000790(n):
    c = 4
    while pow(n,c,c) != (n % c) or isprime(c):
        c += 1
    return c
def A008281gen(): # generator of terms
    blist = [1]
    while True:
        yield from blist
        blist = [0]+list(accumulate(reversed(blist)))
@lru_cache(maxsize=None)
def A015631(n):
    if n == 0:
        return 0
    c, j = 1, 2
    k1 = n//j
    while k1 > 1:
        j2 = n//k1 + 1
        c += (j2-j)*A015631(k1)
        j, k1 = j2, n//j2
    return n*(n-1)*(n+4)//6-c+j
def A046447gen(): # generator of terms
    yield 1
    m = 4
    while True:
        k = nextprime(m)
        for n in range(m,k):
            if (s:=''.join([str(p)*e for p,e in sorted(factorint(n).items())])) == s[::-1]:            
                yield n
        m = k+1
def A057708gen(): # generator of terms
    m = 2
    for k in count(1):
        if isprime(int(str(m)[::-1])): yield k
        m *= 2    
def A063454(n):
    ndict = {}
    for i in range(n):
        m = pow(i,3,n)
        if m in ndict:
            ndict[m] += 1
        else:
            ndict[m] = 1
    count = 0
    for i in ndict:
        ni = ndict[i]
        for j in ndict:
            k = (i+j) % n
            if k in ndict:
                count += ni*ndict[j]*ndict[k]
    return count      
def A350244gen():
    yield 1
    k, b, bdict = 1, 0, {1:(1,),0:(2,)}
    for n in count(3):
        if len(l := bdict[b]) > 1:
            m = (n-1-l[-2])*b
            if m in bdict:
                bdict[m] = (bdict[m][-1],n)
            else:
                bdict[m] = (n,)
            b = m
        else:
            bdict[1] = (bdict[1][-1],n)
            b = 1
        if b > k:
            k = b
            yield n 
def A069942gen(): return filter(lambda n:sum(map(lambda x: int(str(x)[::-1]) if x < n else 0, divisors(n))) == int(str(n)[::-1]),count(1))
def A071869gen(): # generator of terms
    p, q, r = 1, 2, 3
    for n in count(2):
        p, q, r = q, r, max(factorint(n+2))
        if p < q < r:
            yield n
def A071870gen(): # generator of terms
    p, q, r = 1, 2, 3
    for n in count(2):
        p, q, r = q, r, max(factorint(n+2))
        if p > q > r:
            yield n
def A076197gen(): # generator of terms
    g = 1
    for i in count(3,2):
        g *= i
        if is_prime(g+1024):
            yield i
@lru_cache(maxsize=None)
def A090026(n):
    if n == 0:
        return 0
    c, j = 1, 2
    k1 = n//j
    while k1 > 1:
        j2 = n//k1 + 1
        c += (j2-j)*A090026(k1)
        j, k1 = j2, n//j2
    return (n+1)**4-c+15*(j-n-1)
@lru_cache(maxsize=None)
def A090027(n):
    if n == 0:
        return 0
    c, j = 1, 2
    k1 = n//j
    while k1 > 1:
        j2 = n//k1 + 1
        c += (j2-j)*A090027(k1)
        j, k1 = j2, n//j2
    return (n+1)**5-c+31*(j-n-1)
@lru_cache(maxsize=None)
def A090028(n):
    if n == 0:
        return 0
    c, j = 1, 2
    k1 = n//j
    while k1 > 1:
        j2 = n//k1 + 1
        c += (j2-j)*A090028(k1)
        j, k1 = j2, n//j2
    return (n+1)**6-c+63*(j-n-1)
@lru_cache(maxsize=None)
def A090029(n):
    if n == 0:
        return 0
    c, j = 1, 2
    k1 = n//j
    while k1 > 1:
        j2 = n//k1 + 1
        c += (j2-j)*A090029(k1)
        j, k1 = j2, n//j2
    return (n+1)**7-c+127*(j-n-1)
def A114146(n): return 1 if n == 0 else 8*n**2-12*n+6 + 4*sum(totient(i)*(n-i)*(2*n-i) for i in range(2, n))
def A153679gen(): # generator of terms
    n, k, q = 1024, 1000, 0
    for m in count(1):
        r = n % k
        if r > q:
            q = r
            yield m
        n *= 1024
        k *= 1000
        q *= 1000
def A166374gen(): return filter(lambda n:sum([int(n*e/p) for p,e in factorint(n).items()]) == totient(n), count(1))
def A350253(n): return 1 if (m := n % 6) == 2 or m == 5 else (fibonacci(n+1) if m == 3 else fibonacci(n))
def A195269(n):
    m, s = 1, '0'*n
    for i in count(1):
        m *= 3
        if s in str(m): return i
def A230891gen(): # generator of terms
    yield from [0,11]
    l, s, b = Counter('11'), 1, {3}
    while True:
        i = s
        while True:
            if i not in b:
                li, o = Counter(bin(i)[2:]), 0
                for d in (l+li).values():
                    if d % 2:
                        if o > 0:
                            break
                        o += 1
                else:
                    yield int(bin(i)[2:])
                    l = li
                    b.add(i)
                    while s in b:
                        b.remove(s)
                        s += 1
                    break
            i += 1
def A245562gen(): # generator of terms
    yield 0
    for n in count(1): yield from (len(d) for d in split('0+',bin(n)[2:]) if d != '')     
def A247648gen(): return filter(lambda n:n % 2 and not '00' in bin(n),count(1))
def A274086(n): return int((n*tan(n)).round())
def A274087(n): return int((n**2*sin(n)).round())
def A274088(n): return int((n**2*sin(sqrt(n))).round())
def A274090(n): return int((n**2*cos(sqrt(n))).round()) 
def A274091(n):
    k, j = divmod(n,2)
    return int((k**2*sin(sqrt(k)+j*pi/2)).round())
def A274092(n):
    k, j = divmod(n,3)
    return int((k**2*sin(sqrt(k)+j*pi/2)).round())
def A274095(n): return int((n*sin(sqrt(n))).round())
def A274097(n):
    k, j = divmod(n,3)
    return int((k*sin(sqrt(k)+j*pi/2)).round())
def A317085(n):
    c = 1
    for d in partitions(n,m=n*2//3):
        l = len(d)
        if l > 0:
            k = sorted(d.keys())
            for i in range(l//2):
                if d[k[i]] != d[k[l-i-1]]:
                    break
            else:
                c += 1
    return c
def A320485(n): return (lambda x: int(x) if x != '' else -1)(''.join(d if str(n).count(d) == 1 else '' for d in str(n)))
def A328095gen(): return filter(lambda n:(sn := str(n)) in str(n*prod(int(d) for d in sn)), count(0))
def A337856(n):
    k, n1, n2, pset = 0, 10**(n-1)//2-18, 10**n//2-18, set()
    while 50*k**2+60*k < n2:
        a, b = divmod(n1-30*k,50*k+30)
        m = max(k,a+int(b>0))
        r = 50*k*m+30*(k+m)
        while r < n2:
            pset.add(r)
            m += 1
            r += 50*k+30
        k += 1
    return len(pset)
def A345687(n): return pvariance(n**2*u for u, v, w in (igcdex(x,y) for x in range(1,n+1) for y in range(1,n+1)))
def A003512(n): return 2*n + int(isqrt(3*n**2))
def A004720(n):
    l = len(str(n-1))
    m = (10**l-1)//9
    k = n + l - 2 + int(n+l-1 >= m)
    return 0 if k == m else int(str(k).replace('1',''))
def A005487gen(): # generator of terms
    blist, bset = [0,4], {0,4}
    yield from blist
    for i in count(0):
        n, flag = blist[-1]+1, False
        while True:
            for j in range(i+1,0,-1):
                m = 2*blist[j]-n
                if m in bset:
                    break
                if m < 0:
                    flag = True
                    break
            else:
                blist.append(n)
                bset.add(n)
                yield n
                break
            if flag:
                blist.append(n)
                bset.add(n)
                yield n
                break
            n += 1
def A006723gen(): # generator of terms
    blist= [1]*7
    yield from blist
    while True:
        blist = blist[1:]+[(blist[-1]*blist[-6]+blist[-2]*blist[-5]+blist[-3]*blist[-4])//blist[-7]]
        yield blist[-1]
def A007487(n): return n**2*(n**2*(n**2*(n**2*(n*(2*n + 10) + 15) - 14) + 10) - 3)//20
def A008559gen(): # generator of terms
    b = 2
    while True:
        yield b
        b = int(bin(b)[2:])
def A027602(n): return n*(n*(3*n + 9) + 15) + 9
def A029976gen(): return filter(isprime,palQgen(8))
def A029997gen(): return filter(lambda n:gmpy2digits(n,11) == gmpy2digits(n,11)[::-1],(n**2 for n in count(0)))
def A036967gen(): return filter(lambda n:min(factorint(n).values(),default=4) >= 4,count(1))
def A048543(n):
    k, m = 1, 2
    while True:
        if str(m).count('7') == n:
            return k
        k += 1
        m += 2*k
def A048544(n):
    k, m = 1, 2
    while True:
        if str(m).count('7') == n:
            return m
        k += 1
        m += 2*k
def A053165(n): return 1 if n <=1 else prod(p**(e % 4) for p,e in factorint(n).items())
def A054383gen(): # generator of terms
    l = {}
    for d in permutations('123456789', 9):
        for i in range(8):
            s1, s2 = int(''.join(d[:i+1])), int(''.join(d[i+1:]))
            q, r = divmod(s1,s2)
            if not r:
                if q in l:
                    l[q] += 1
                else:
                    l[q] = 1
    for i in count(1):
        if i in l:
            yield l[i]
        else:
            yield 0
def A055155(n): return sum(gcd(d,n//d) for d in divisors(n,generator=True))
def A058411gen(): return filter(lambda i:i % 10 and max(str(i**2)) < '3',count(0))
def A064834(n):
    x, y = str(n), 0
    lx2, r = divmod(len(x),2)
    for a,b in zip(x[:lx2],x[:lx2+r-1:-1]):
        y += abs(int(a)-int(b))
    return y   
def A065714(n): return str(2**n).count('3') 
def A065716(n): return str(2**n).count('5') 
def A065717(n): return str(2**n).count('6')
def A065718(n): return str(2**n).count('7')
def A065744(n): return str(2**n).count('9')
def A073785(n):
    s, q = '', n
    while q >= 3 or q < 0:
        q, r = divmod(q, -3)
        if r < 0:
            q += 1
            r += 3
        s += str(r)
    return int(str(q)+s[::-1])
def A073786(n):
    s, q = '', n
    while q >= 5 or q < 0:
        q, r = divmod(q, -5)
        if r < 0:
            q += 1
            r += 5
        s += str(r)
    return int(str(q)+s[::-1])
def A073787(n):
    s, q = '', n
    while q >= 6 or q < 0:
        q, r = divmod(q, -6)
        if r < 0:
            q += 1
            r += 6
        s += str(r)
    return int(str(q)+s[::-1])
def A073788(n):
    s, q = '', n
    while q >= 7 or q < 0:
        q, r = divmod(q, -7)
        if r < 0:
            q += 1
            r += 7
        s += str(r)
    return int(str(q)+s[::-1])
def A073789(n):
    s, q = '', n
    while q >= 8 or q < 0:
        q, r = divmod(q, -8)
        if r < 0:
            q += 1
            r += 8
        s += str(r)
    return int(str(q)+s[::-1])
def A073790(n):
    s, q = '', n
    while q >= 9 or q < 0:
        q, r = divmod(q, -9)
        if r < 0:
            q += 1
            r += 9
        s += str(r)
    return int(str(q)+s[::-1])
def A066417(n): return 0 if n == 1 else divisor_sigma(2*n-1)+divisor_sigma(2*n+1)+divisor_sigma(n//2**(k:=multiplicity(2,n)))*2**(k+1)-6*n-2
def A073930gen(): return filter(lambda n:divisor_sigma(2*n-1)+divisor_sigma(2*n+1)+divisor_sigma(n//2**(k:=multiplicity(2,n)))*2**(k+1)-7*n-2==0,count(2))
def A192268gen(): return filter(lambda n:divisor_sigma(2*n-1)+divisor_sigma(2*n+1)+divisor_sigma(n//2**(k:=multiplicity(2,n)))*2**(k+1)-7*n-2 > 0,count(2))
def A082410(n):
    if n == 1:
        return 0
    s = bin(n-1)[2:]
    m = len(s)
    i = s[::-1].find('1')
    return 1-int(s[m-i-2]) if m-i-2 >= 0 else 1
def A111116gen(): return filter(lambda n:len(set(str(n)) & set(str(n**4)))==0, count(1))
def A115927gen(): # generator of terms
    l = {}
    for d in permutations('0123456789', 10):
        if d[0] != '0':
            for i in range(9):
                if d[i++1] != '0':
                    q, r = divmod(int(''.join(d[:i+1])), int(''.join(d[i+1:])))
                    if not r:
                        if q in l:
                            l[q] += 1
                        else:
                            l[q] = 1
    for i in count(1):
        if i in l:
            yield l[i]
        else:
            yield 0
def A235811gen(): return filter(lambda n:len(set(str(n**3))) == 9,count(0))
def A235809gen(): return filter(lambda n:len(set(str(n**3))) == 7,count(0))
def A137921(n): return len([d for d in divisors(n,generator=True) if n % (d+1)])
def A153686gen(): # generator of terms
    k10, k11 = 10, 11
    for k in count(1):
        if (k11 % k10)*k < k10:
            yield k
        k10 *= 10
        k11 *= 11
def A153670gen(): # generator of terms
    k10, k11 = 100, 101
    for k in count(1):
        if (k11 % k10)*k < k10:
            yield k
        k10 *= 100
        k11 *= 101
def A153687gen(): # generator of terms
    n, k, q = 11, 10, 0
    for m in count(1):
        r = n % k
        if r > q:
            q = r
            yield m
        n *= 11
        k *= 10
        q *= 10
def A177029gen(): # generator of terms
    for m in count(1):
        n, c = 3, 0
        while n*(n+1) <= 2*m:
            if not 2*(n*(n-2) + m) % (n*(n - 1)):
                c += 1
                if c > 1:
                    break
            n += 1
        if c == 1:
            yield m
def A187824(n):
    k = 1
    while (n+1) % k < 3:
        k += 1
    return k-1
def A206709(n):
    c, b, b2, n10 = 0, 1, 2, 10**n
    while b <= n10:
        if isprime(b2):
            c += 1
        b += 1
        b2 += 2*b - 1
    return c
def A219531(n): return n*(n*(n*(n*(n*(n*(n*(n*(n*(n*(n - 44) + 935) - 11550) + 94083) - 497112) + 1870385) - 3920950) + 8550916) + 4429656) + 29400480)//39916800 + 1
def A226561(n): return sum(totient(d)*d**n for d in divisors(n,generator=True))
def A228640(n): return sum(totient(d)*n**(n//d) for d in divisors(n,generator=True))
def A242171gen(): # generator of terms
    yield 1
    bell_list, blist, b = [1,1], [1], 1
    while True:
        blist = list(accumulate([b]+blist))
        b = blist[-1]
        fs = primefactors(b)
        for p in fs:
            if all(n % p for n in bell_list):
                yield p
                break
        else:
            yield 1
        bell_list.append(b)
def A245563gen(): yield from chain([0],(len(d) for n in count(1) for d in split('0+',bin(n)[:1:-1]) if d != ''))
def A246588(n): return prod(bin(len(d)).count('1') for d in split('0+',bin(n)[2:]) if d) if n > 0 else 1
def A246595(n): return prod(len(d)**2 for d in split('0+',bin(n)[2:]) if d != '') if n > 0 else 1
def A246596(n):
    s, c = bin(n)[2:], [1, 1]
    for m in range(1, len(s)):
        c.append(c[-1]*(4*m+2)//(m+2))
    return prod(c[len(d)] for d in split('0+',s)) if n > 0 else 1
def A247649gen(): # generator of terms
    from sympy.abc import x
    f, g, blist = 1/x**2+1/x+1+x+x**2, 1, [1]
    yield 1
    for n in count(1):
        s = [int(d,2) for d in bin(n)[2:].split('00') if d != '']
        g = (g*f).expand(modulus=2)
        if len(s) == 1:
            blist.append(g.subs(x,1))
            yield blist[-1]
        else:
            blist.append(prod(blist[d] for d in s))
            yield blist[-1]
def A225654gen(): # generator of terms
    from sympy.abc import x
    f, g, blist, c = 1/x**2+1/x+1+x+x**2, 1, [1], 1
    yield c
    for n in count(1):
        s = [int(d,2) for d in bin(n)[2:].split('00') if d != '']
        g = (g*f).expand(modulus=2)
        if len(s) == 1:
            blist.append(g.subs(x,1))
        else:
            blist.append(prod(blist[d] for d in s))
        c += blist[-1]
        yield c
def A254449(n):
    if n == 0:
        return 0
    i, m, s = 1, 1, '4'*n
    s2 = s+'4'
    while True:
        m *= i
        sn = str(m)
        if s in sn and s2 not in sn:
            return i
        i += 1            
def A266142(n): return 4*n if (n==1 or n==2) else sum(1 for d in range(-3,7) for i in range(n) if isprime((10**n-1)//3+d*10**i))
def A266146(n): return 4*n if (n==1 or n==2) else sum(1 for d in range(-7,3) for i in range(n) if isprime(7*(10**n-1)//9+d*10**i))
def A266148(n): return sum(1 for d in range(-9,1) for i in range(n) if isprime(10**n-1+d*10**i))
def A289673gen(): return (-1 if s == ('1',) else int((''.join(s)+('2212' if s[0] == '2' else '11'))[3:]) for l in count(1) for s in product('12',repeat=l))
def A305611(n):
    fs = factorint(n)
    return len(set(sum(d) for i in range(1,sum(fs.values())+1) for d in multiset_combinations(fs,i)))
def A317088(n):
    if n == 0:
        return 1
    c = 0
    for d in partitions(n,k=isqrt(2*n)):
        l = len(d)
        if l > 0 and l == max(d):
            v = set(d.values())
            if len(v) == max(v):
                c += 1
    return c
def A345688(n): return pvariance(n**2*v for u, v, w in (igcdex(x,y) for x in range(1,n+1) for y in range(1,n+1)))
def A004721(n):
    l = len(str(n))
    m = 2*(10**l-1)//9
    k = n + l - int(n+l < m)
    return 1 if k == m else int(str(k).replace('2','')) 
def A004722(n):
    l = len(str(n))
    m = (10**l-1)//3
    k = n + l - int(n+l < m)
    return 2 if k == m else int(str(k).replace('3','')) 
def A004724(n):
    l = len(str(n))
    m = 5*(10**l-1)//9
    k = n + l - int(n+l < m)
    return 4 if k == m else int(str(k).replace('5','')) 
def A004731(n):
    if n <= 1:
        return 1
    a, b = factorial2(n-2), factorial2(n-1)
    return b//gcd(a,b)
def A011968gen(): # generator of terms
    yield from [1,2]
    blist, b = [1], 1
    while True:
        blist = list(accumulate([b]+blist))
        yield b+blist[-1]
        b = blist[-1]
def A014710(n):
    s = bin(n+1)[2:]
    m = len(s)
    i = s[::-1].find('1')
    return 2-int(s[m-i-2]) if m-i-2 >= 0 else 2      
def A017713gen(): # generator of terms
    m = [1]*50
    while True:
        yield m[-1]
        for i in range(49):
            m[i+1] += m[i]
def A017713(n): return comb(n,49)
def A020462gen(): return filter(isprime,(int(''.join(x)) for n in count(1) for x in product('35',repeat=n)))
@lru_cache(maxsize=None)
def A022825(n):
    if n <= 1:
        return n
    c, j = 0, 2
    k1 = n//j
    while k1 > 1:
        j2 = n//k1 + 1
        c += (j2-j)*A022825(k1)
        j, k1 = j2, n//j2
    return c+n+1-j 
def A030665(n):
    d, nd = 10, 10*n
    while True:
        x = nextprime(nd)
        if x < nd+d:
            return int(x)
        d *= 10
        nd *= 10 
def A050932(n): return (q := bernoulli(n).q)//gcd(q,n+1)