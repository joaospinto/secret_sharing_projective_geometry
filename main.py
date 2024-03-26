#####################
### use: script() ###
#####################

from math import sqrt
from random import randint

global n,d,p,K1,K2

# Zp field

class Zp:
    def __init__(self,n):
        self.value = (n%p)
    def __eq__(a,b):
        return a.value==b.value
    def __str__(self):
        return "[%d]" % self.value
    def __add__(a,b):
        return Zp(a.value+b.value)
    def __mul__(a,b):
        return Zp(a.value*b.value)
    def __sub__(a,b):
        return Zp(a.value-b.value)
    def __neg__(self):
        return Zp(-self.value)
    def __repr__(self):
        return "Zp(%d)" % self.value

def inverse(self): # for big p values it would be convenient to use a faster process
    i=1
    while i<p:
        x=Zp(i*self.value)
        if x.value==1:
            return Zp(i)
        i+=1
    raise ValueError

# definition of global variables

print("This program provides (t,n) threshold schemes for sharing integers using vector spaces over finite fields")
n=int(input("How many people will share the secret (n)? "))
t=int(input("How many shares are needed to break the secret (t)? "))
m=int(input("How many different secrets shall there be? "))

def isprime(q):
    s=sqrt(q)
    i=2
    while i<=s:
        if q%i==0:
            return False
        i+=1
    return True

def ffprime(q):
    i=q
    while True:
        if isprime(i):
            return i
        i+=1

def null_vector(dim):
    v=[]
    i=0
    while i<dim:
        v.append(Zp(0))
        i+=1
    return v

p=ffprime(m)
d=t+1
K1=null_vector(d)
K2=null_vector(d)
K1[0]=Zp(1)
K2[1]=Zp(1)

# script

def script():
    b=int(input("Encrypt without checking(1), encrypt safely (2), decrypt(3) or exit(4)? "))
    if b==1:
        secret=int(input("What is the secret? "))
        print(vector_generator(secret))
    elif b==2:
        secret=int(input("What is the secret? "))
        print(vector_generator_safe(secret))
    elif b==3:
        code=input("What is the code? ")
        secret=descodifica(eval(code))
        print(secret)

# matrices over Zp

def converte(lista_dupla):
    for lista in lista_dupla:
        for i in range(len(lista)):
            if type(lista[i])==int:
                lista[i]=Zp(lista[i])

def linha_nula(linha):
    for x in linha:
        if not x==Zp(0):
            return False
    return True

def subtrair(linha1,linha2):
    l=len(linha1)
    lst=[]
    i=0
    while i<l:
        lst.append(linha1[i]-linha2[i])
        i+=1
    return lst

def simplify(vector):
    l=len(vector)
    i=0
    while i<l:
        if not vector[i]==Zp(0):
            return sv_mult(inverse(vector[i]),vector)
        i+=1
    return vector

def uniformiza(matriz):
    m=len(matriz)
    t=0
    while t<m:
        matriz[t] = simplify(matriz[t])
        t+=1

def pivot(matriz,coluna):
    m=len(matriz)
    n=len(matriz[0])
    i=0
    while i<m:
        j=0
        while j<coluna:
            if not matriz[i][j]==Zp(0):
                break
            j+=1
        else: #j==coluna
            if not matriz[i][j]==Zp(0):
                return i
        i+=1
    return m

def reduz_coluna(matriz,coluna):
    m=len(matriz)
    uniformiza(matriz)
    p=pivot(matriz,coluna)
    if p!=m:
        j=0
        while j<m:
            if j==p or matriz[j][coluna]==Zp(0):
                j+=1
                continue
            matriz[j]=subtrair(matriz[j],matriz[p])
            j+=1

def conta_linhas_zeros(mg):
    m=len(mg)
    n=len(mg[0])
    c=0
    i=0
    while i<m:
        j=0
        while j<n:
            if not mg[i][j]==Zp(0):
                break
            j+=1
        else:
            c+=1
        i+=1
    return c

def gauss_elimination(mtx):
    matriz=mtx[:]
    n=len(matriz[0])
    converte(matriz)
    i=0
    while i<n:
        reduz_coluna(matriz,i)
        i+=1
    return matriz

def rank(mtx): # the input must be a matrix in its row-echelon form
    return len(mtx)-conta_linhas_zeros(mtx)

def transpose(matrix):
    mt=[]
    m=len(matrix)
    n=len(matrix[0])
    i=0
    while i<n:
        j=0
        v=[]
        while j<m:
            v.append(matrix[j][i])
            j+=1
        mt.append(v)
        i+=1
    return mt

# vector space of dimension d over Zp

def sv_mult(a,b):
    c=[]
    for x in b:
        c.append(a*x)
    return c

def independent(lv):
    return len(lv)==rank(gauss_elimination(lv))

def vector_sum(u1,u2):
    l=len(u1)
    v=[]
    i=0
    while i<l:
        v.append(u1[i]+u2[i])
        i+=1
    return v

def int_to_Zp(l1):
    l2=[]
    for x in l1:
        l2.append(Zp(x))
    return l2

# encrypting

def find_intersection(lv1,lv2):
    mt=transpose(lv1[0:d-1]+lv2)
    mt=gauss_elimination(mt)
    c1=mt[d-1][d-1]
    c2=mt[d-1][d]
    a1=-inverse(c1)*c2
    v=vector_sum(sv_mult(a1,lv2[0]),lv2[1])
    return simplify(v)

def codifica(segredo):
    return vector_sum(K1,sv_mult(Zp(segredo),K2))

def descodifica(codigo):
    v=simplify(find_intersection(codigo,[K1,K2]))
    return v[1].value%p

def combinacoes(m,x):
    lf=[]
    i=[]
    k=0
    while k<x:
        i.append(k)
        k+=1
    lf.append(i[:])
    while True:
        k=1
        while k<=x:
            if i[x-k]<m-k:
                i[x-k]=i[x-k]+1
                tmp=i[x-k]
                j=1
                while j<k:
                    i[x-k+j]=tmp+j
                    j+=1
                break
            k+=1
        else:
            break
        lf.append(i[:])
    return lf

def vector_generator(segredo):
    vl1=[]
    i=0
    while i<d-2:
        j=0
        vtemp=[]
        while j<d:
            vtemp.append(Zp(randint(0,p-1)))
            j+=1
        vl1.append(simplify(vtemp))
        i+=1
    vl1.append(codifica(segredo))
    vl2=[]
    i=0
    while i<n:
        j=0
        c=[]
        while j<d-1:
            c.append(Zp(randint(1,p-1))) #c[0] must not be 0
            j+=1
        vtemp=null_vector(d)
        j=0
        while j<d-1:
            vtemp=vector_sum(vtemp,sv_mult(c[j],vl1[j]))
            j+=1
        vl2.append(vtemp)
        i+=1
    return vl2

def vector_generator_safe(segredo):
    while True:
        sinal=False
        vl=vector_generator(segredo)
        llist=combinacoes(n,d-2)
        for l in llist:
            lv=[K1,K2]
            for x in l:
                lv.append(vl[x])
            if not independent(lv):
                sinal=True
        if sinal==False:
            break
    return vl

if __name__ == "__main__":
    script()
