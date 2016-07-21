import matplotlib.pyplot as plt
import numpy as np
import csv
from sklearn import datasets, linear_model
from math import exp, log, sqrt
from decimal import *

class Predictor():
    param = []

    def genera_sd(self, v, sd):
        	lista = []
        	for i in range(-8,11):
        		lista.append(v + 0.25*sd*i)
        	return lista

    def calcula_inr(self, Dose, vec_param):
        m = vec_param[0]
        Cl = vec_param[1]
        V = vec_param[2]
        k = vec_param[3]
        Tau = vec_param[4]
        Cmax = vec_param[5]    
        #inr <- ((1/(-(m*Cl/V)/(k^2)*(1-(k*Tau/24)/(1-exp(-k*Tau/24)))-(m/k)*log((Dose/V)/(Cmax*(1-exp(-(Cl/V)*(Tau/24))))))+3.36)/4.368)^(1/0.383)    
        B = (-m*Cl/V)/(k**2)
        C = 1.-(k*Tau/24.)/(1.-exp(-k*Tau/24.))
        try:
        	D = (m/k)*log((Dose/V)/(Cmax*(1.-exp(-(Cl/V)*(Tau/24.)))))
        except:
        	D = -float("inf")
        try:
        	inr = ( (1./(B*C-D) + 3.36)/4.368 )**(1./0.383)
        except:
        	inr = float("nan")  
        return inr

    def calcula_mejor_curva(self, dosis, inr):
        d = 0 
        dif = 100 
        curva = []
        for i in range (0, len(self.param)):
            pred_inr = self.calcula_inr(dosis/7, self.param[i])
            d = sqrt(pow((float(inr) - pred_inr),2))
            if d < dif:
                dif = d 
                curva = i + 1
        dif = 100 
        return curva
        
    def calcula_dosis(self, INR_T, curva):
        vec_param = self.param[curva-1]
        m = vec_param[0]
        Cl = vec_param[1]
        V = vec_param[2]
        k = vec_param[3]
        Tau = vec_param[4]
        Cmax = vec_param[5]
        B = (-m*Cl/V)/(k**2)
        C = 1.-(k*Tau/24.)/(1.-exp(-k*Tau/24.))
        E = B*C - 0.2289377/(INR_T**0.383 - 0.7692308)
        dosis = V*Cmax*(1.-exp(-Cl*Tau/(24.*V)))*exp(E*k/m)
        dosis = round(dosis*7,0)
        return dosis

    def __init__(self):
        lista_m = self.genera_sd(0.422, 0.1043)
        lista_k = self.genera_sd(0.98, 0.17)
        lista_cmax = self.genera_sd(5.49, 1.63)
        lista_Cl = [2.19]*19
        lista_V = [7.5]*19
        lista_Tau = [24.]*19
        dosis = [0, 0.25, 0.5, 1., 1.5, 2., 2.5, 3., 3.5, 4., 4.5, 5., 5.5, 6., 6.5, 7., 7.5, 8., 8.5, 9., 9.5, 10, 10.5, 11, 11.5, 12, 12.5, 13, 13.5, 14, 14.5, 15, 15.5, 16, 16.5, 17]
        self.param.append(lista_m)
        self.param.append(lista_Cl)
        self.param.append(lista_V)
        self.param.append(lista_k)
        self.param.append(lista_Tau)
        self.param.append(lista_cmax)
        self.param = [list(i) for i in zip(*self.param)]

    #Valores predeterminados.
    #m = 0.422
    #Cl = 2.19
    #V = 7.5
    #k = 0.98
    #Dose = 0.5
    #Tau = 1.
    #Cmax = 5.49

    #print(calcula_mejor_curva(param, paciente))
    #print(calcula_dosis(2.5, param, 8))
