import math
hf = 85.0
L = 24000
d = 0.203
v = 1.3*pow(10,-4)
beta = 0.0246
m = 0.25
a=hf*math.pow(d,5.0-m)
print("a："+str(a))
b=beta*L*math.pow(v,m)
print("b："+str(b))
e=a/b
print("e："+str(e))
c=1.0/(2.0-m)
print("c："+str(c))
Q=math.pow(e,c)
print("Q："+str(Q))
Re=4*Q/(math.pi*d*v)
print("Re0："+str(Re))
if(Re<2300):
    beta=4.15
    Q = hf * pow(d, 4) / (beta * v * L)
    Re = 4 * Q / (math.pi * d * v)
    print("Re：" + str(Re))
    print("Q：" + str(Q))
print("Re："+str(Re))
print("Q："+str(Q))