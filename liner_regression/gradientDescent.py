
#coding=utf-8
"""
y = ax + b
L = ( y_ - y )^2 = ( ax + b - y_ )^2
∂L/∂a = 2x
∂L/∂b = 1

"""
import sys
from matplotlib import pyplot as plt
x = [1,2,3,4,5]
y = tuple(map(lambda i: i * 100 + 10,x))
a = 1000
b = -1000
import time
def f(x):
    return a * x + b
def loss(): 
    N = len(x)
    return sum( map(lambda i: (f(x[i])-y[i]) ** 2,range(0,N)))/N
learn_rate = 0.1
plt.show()
for i in range(10000):
    N = len(x)
    temp0 = sum( map(lambda i: (f(x[i])-y[i]) * x[i] ,range(0,N))) / N
    temp1 = sum( map(lambda i: (f(x[i])-y[i])  ,range(0,N))) / N
    a -= learn_rate * temp0
    b -= learn_rate * temp1         
    print(a,b,loss(),temp0,temp1,f(x[0]),y[0])
    time.sleep(0.01)