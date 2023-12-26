from gmpy2 import *
from Crypto.Util.number import *
from primefac import *
def know_pqec(factors:list,e:int,c:int):
    '''
    :param factors: 因子列表
    :param e: 公钥
    :param c: 密文
    :return: 明文
    '''
    n=1
    phi=1
    factor_l=[]
    for _ in range(len(factors)):
        n*=factors[_]
    for _ in factors:
        if _ not in factor_l:
            factor_l.append(_)
    for factor in factor_l:
        phi=phi*(factor-1)*pow(factor,factors.count(factor)-1)
    d=int(invert(e,phi))
    m=pow(c,d,n)
    return long_to_bytes(int(m))

def small_e(e:int,c:int):
    '''
    低加密指数攻击
    '''
    m=int(iroot(c,e)[0])
    return long_to_bytes(m)
# ZmxhZ3tUaGlzX20xZ2h0X3cwcmtfRm9yX3kwdn0=

def know_dp(n:int,e:int,dp:int,c:int):
    '''
    已知dp
    '''
    for k in range(1,e):
        if (e*dp-1)%k==0:
            p=(e*dp-1)//k+1
            if n%p==0:
                q=n//p
                return know_pqec([p,q],e,c)

def know_pqdpdq(p:int,q:int,dp:int,dq:int,c:int):
    '''
    已知dp，dq
    '''
    n=p*q
    phi=(p-1)*(q-1)
    dd=gcd(p-1,q-1)
    d=(dp-dq)//dd*int(invert((q-1)//dd,(p-1)//dd))*(q-1)+dq
    return long_to_bytes(int(pow(c,int(d),n)))

def wiener_attack(n:int,e:int,c:int):
    '''
    维纳攻击，当d满足d<1/3*n^(1/4)时
    '''
    def transform(x, y):
        arr = []
        while y:
            arr += [x // y]
            x, y = y, x % y
        return arr

    def sub_fraction(k):
        x = 0
        y = 1
        for i in k[::-1]:
            x, y = y, x + i * y
        return (y, x)
    con=transform(e,n)
    for i in range(1,len(con)+1):
        data=con[:i]
        d=sub_fraction(data)[1]
        m=pow(c,d,n)
        flag=long_to_bytes(m)
        if b'flag' or b'CTF' or b'ctf' in flag:
            return flag

def continue_fra(x,y):
    def transform(x, y):
        arr = []
        while y:
            arr += [x // y]
            x, y = y, x % y
        return arr
    def sub_fraction(k):
        x = 0
        y = 1
        for i in k[::-1]:
            x, y = y, x + i * y
        return (y, x)
    con=transform(x,y)
    denominator=[]
    numerator=[]
    for i in range(1,len(con)+1):
        data=con[:i]
        denominator.append(sub_fraction(data)[1])
        numerator.append(sub_fraction(data)[0])
    return denominator,numerator

def common_moudle(n:int,e1:int,e2:int,c1:int,c2:int):
    if gcd(e1,e2)==1:
        _,s1,s2=gcdext(e1,e2)
        m=pow(c1,s1,n)*pow(c2,s2,n)%n
        return long_to_bytes(m)
    else:
        g=gcd(e1,e2)
        e1=e1//g
        e2=e2//g
        _, s1, s2 = gcdext(e1, e2)
        m = pow(c1, s1, n) * pow(c2, s2, n) % n
        return long_to_bytes(int(iroot(m,g)[0]))

def Pollard_attack(n:int):
    # Pollard's p-1
    a = 2
    k = 2
    while True:
        a = powmod(a, k, n)
        res = gcd(a - 1, n)
        if res != 1 and res != n:
            q = n // res
            return res,q
        k+=1

def Williams_attack(n:int):
    # Williams's p+1
    return williams_pp1(n)
















    