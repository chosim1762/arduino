from umatrix import *
from machine import Pin, I2C
from ssd1306 import SSD1306_I2C
import math
import array

def xy2uv(A, B, xy):
    x = matrix([xy[0]],[xy[1]])
    [[uf],[vf]] = A*x + B
    u = round(uf)
    v = round(vf)
    return u, v

def AB(um,vm,xyb):
    uv = (um-1,vm-1)
    A = (matrix([uv[0],0],[0,uv[1]]) *
        matrix(
            [xyb[1][0]-xyb[0][0], xyb[2][0]-xyb[0][0]],
            [xyb[1][1]-xyb[0][1], xyb[2][1]-xyb[0][1]]
        ).inverse)
    B = -A*matrix([xyb[0][0]],[xyb[0][1]])
    return A, B

um = 72
vm = 40

i2c  = I2C(0, scl=Pin(6), sda=Pin(5), freq=40000)
oled = SSD1306_I2C(um, vm, i2c)

def func(x):
    return 2 * math.sin(x / 20 * 1) + 1

xs = array.array('i', [i for i in range(300)])
ys = array.array('f', [func(x) for x in range(300)])

xmin = min(xs)
xmax = max(xs)
ymin = min(ys)
ymax = max(ys)

xyb = [[xmin,ymax],[xmax,ymax],
       [xmin,ymin],[xmax,ymin]]

A, B = AB(um,vm,xyb)

oled.fill(0)
oled.rect(0,0,um-1,vm-1,1)
for i, x in enumerate(xs):
    u, v = xy2uv(A, B, (x,ys[i]))
    oled.pixel(u, v, 1)
    oled.show()