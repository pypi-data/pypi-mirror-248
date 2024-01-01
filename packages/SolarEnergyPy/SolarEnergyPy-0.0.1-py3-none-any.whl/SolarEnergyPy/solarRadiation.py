__author__ = ' He Liqun '
import pendulum
import math
import numpy
from fractions import Fraction
from .solarPosition import *

class solarRadiation(solarPosition):
    solar_constant = 1367  # W/m^2
    Gsc = solar_constant

    def __init__(self):
        super().__init__()

    def __str__(self):
        return f'{self.constant:0.1f} W/m^2'

    @property
    def constant(self):
        return self.solar_constant

    def Gon_generator(self,n):
        if isinstance(n,(list,tuple,range)) :
            m = n
        else:
            m = range(n)
        for i in m:
            yield self.Gon(i)

    def Gon(self, n = None , precise=None):
        m = n if n is not None else self.day_of_year
 
        G = self.Gsc * self.simple_equation(m)
        if not precise is None:
            G = self.Gsc * self.Spencer_equation(m)
        return G

    def simple_equation(self,n=1):
        B = 360 * n / super().days_of_one_year
        var = 1 + 0.033 * cosd(B)
        return var

    def Spencer_equation(self, n=1):
        #n  = super().day_of_year
        B  = 360 * (n-1) / super().days_of_one_year
        var = 1.00011 + 0.034221 * cosd(B) + 0.001280 * sind(B) + 0.000719 * cosd(2*B) * 0.000077 * sind(2*B)
        return var

    def solar_radiation_at(self, at = None, n = None):
 
        if at is not None :
            old = self.clocktime
            self.clocktime = pendulum.instance(at)

        seconds = self.seconds

        m = n if n is not None else self.day_of_year

        Ts = seconds / 3600
        solar_hour_angle = ( Ts - 12 )*15
    
        A  = ( 284 + m  )* 360./self.days_of_one_year
        solar_declination = 23.45*sind(A)

        Phi   = self.latitude
        w     = solar_hour_angle
        Delta = solar_declination

        cosThetaz = cosd( Phi) * cosd( Delta ) * cosd ( w ) + sind( Phi ) * sind( Delta )

        if cosThetaz > cosd(90):
            tb = self.a0 + self.a1 * math.exp(-self.k/cosThetaz) 
            td = 0.271 - 0.294 * tb
        else:
            tb, td = 0,0

        # print(f"Gon = {self.Gon(m)}")
        # print(f" tb,td = {tb,td}")
        if at is not None :
            self.clocktime = old
        return self.Gon(m) * tb, self.Gon(m)* td

    def solar_radiation_during(self, \
             dt1 = datetime(datetime.now().year,1,1,0,0), \
             dt2 = datetime(datetime.now().year,12,31,23,59)):
        start  = pendulum.instance(dt1)
        end    = pendulum.instance(dt2)
        # 初始化当前时间为起始时间
        current_time = start
        
        # 循环计算每个时刻的太阳时
        beams = []
        diffuses  = []

        restore = self.clocktime
        while current_time <= end:
            # 设置当前时间,更新太阳时
            self.clocktime = current_time
            
            # 计算当前时刻的太阳直射与散射辐射
            beam, diffuse = self.solar_radiation_at()
            beams.append(beam)
            diffuses.append(diffuse)

            # 当前时间增加1小时
            current_time = current_time.add(hours=1)

        self.clocktime  = restore
        return beams,diffuses


import matplotlib.pyplot as plt
def demo():
    print(' Demo on how to use the class solarRadiation')
    sr = solarRadiation()
    print(' solar constant = {} W/m^2 '.format(sr))
    print('{:0.4f}'.format(sr.Spencer_equation(165)))

    for i in range(10) :
        print('{0} : {1:0.2f}'.format(i,sr.Gon(i)))

if __name__ == '__main__' :
    demo()