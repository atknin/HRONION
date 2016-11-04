# -*- coding: utf-8 -*-
import time
import math, cmath
from scipy import integrate

wavelength_1 = 0.709300*1e-10 #К альфа 1
wavelength_2 = 0.713590*1e-10 #К альфа 2
S1 = 50*1e-6 # S1=S2 - ширина колимирующих щелей
S2 = 50*1e-6
L1x = 0.54 # L12, L1, L2 - оптические расстояния  между обеими щелями и каждой из двух щелей и рентгеновской трубкой
L12 = 0.45
L2x = L1x+L12
sigmaX = 0.5*1e-3 # полуширина излучающего пятна рентгеновской трубки
b = -1
C = 1

# -----------Аппаратная функция-------------------
def apparatnaya(teta):
	def x1(teta):
		return -(S1/2+abs(teta)*L1x)/(math.sqrt(2)*sigmaX)

	def x2(teta):
		
		if teta_1 >= abs(teta):
			return (S1/2-abs(teta)*L1x)/(math.sqrt(2)*sigmaX) 
			
		elif abs(teta)>=teta_1 and abs(teta)<=teta_2:
			return (S2/2-abs(teta)*L2x)/(math.sqrt(2)*sigmaX) 

	return integrate.quad(lambda x: math.exp(-x*x) ,x1(teta),x2(teta))[0]


#-----------спектральная функция-----------
def g_lambd(itta):

	d_lambd1 = wavelength_1*3e-4
	d_lambd2 = wavelength_2*3e-4
	return 2/(3*math.pi)*((d_lambd1/wavelength_1)/(math.pow((itta-1),2)+math.pow(d_lambd1/wavelength_1,2))+0.5*(d_lambd2/wavelength_1)/(math.pow((itta-wavelength_2/wavelength_1),2)+math.pow((d_lambd2/wavelength_1),2)))

#-----------образец-----------	
def sample_curve(dTeta,teta,itta):

	X0 = -31.745*1e-7 + 0.1606j*1e-7 #-*-на входе-*-
	Xh = 19.210*1e-7 + 0.15j*1e-7 #-*-на входе-*-
	tetaprmtr = 10.6436 #-*-на входе-*-

	sample = dTeta+teta-(itta-1)*math.tan(math.radians(tetaprmtr))
	alfa = -4*math.sin(tetaprmtr)*(math.sin(tetaprmtr+sample)-math.sin(tetaprmtr)) # угловая отстройка падающего излучения от угла Брегга
	prover = (1/4)*(X0*(b+1)-b*alfa+cmath.sqrt(((X0*(b-1)-b*alfa)*(X0*(b-1)-b*alfa))+4*b*(C*C)*((Xh.real)*(Xh.real)-(Xh.imag)*(Xh.imag)-2j*Xh.real*Xh.imag)))
	if prover.imag < 0:
			eps = (1/4)*(X0*(b+1)-b*alfa-cmath.sqrt(((X0*(b-1)-b*alfa)*(X0*(b-1)-b*alfa))+4*b*(C*C)*((Xh.real)*(Xh.real)-(Xh.imag)*(Xh.imag)-2j*Xh.real*Xh.imag)))
	else:
		eps = prover
		
	R=(2*eps-X0)/Xh/C
	return abs(R)*abs(R)
#-----------монохроматор-----------
def monohromator_curve(teta, itta):

	X0 = -31.745*1e-7 + 0.1606j*1e-7 #-*-на входе-*-
	Xh = 19.210*1e-7 + 0.15j*1e-7 #-*-на входе-*-
	tetaprmtr = 10.6436 #-*-на входе-*-

	monohrom = teta-(itta-1)*math.tan(math.radians(tetaprmtr))
	alfa = -4*math.sin(tetaprmtr)*(math.sin(tetaprmtr+monohrom)-math.sin(tetaprmtr)) # угловая отстройка падающего излучения от угла Брегга
	prover = (1/4)*(X0*(b+1)-b*alfa+cmath.sqrt(((X0*(b-1)-b*alfa)*(X0*(b-1)-b*alfa))+4*b*(C*C)*((Xh.real)*(Xh.real)-(Xh.imag)*(Xh.imag)-2j*Xh.real*Xh.imag)))
	if prover.imag < 0:
			eps = (1/4)*(X0*(b+1)-b*alfa-cmath.sqrt(((X0*(b-1)-b*alfa)*(X0*(b-1)-b*alfa))+4*b*(C*C)*((Xh.real)*(Xh.real)-(Xh.imag)*(Xh.imag)-2j*Xh.real*Xh.imag)))
	else:
		eps = prover
		
	R=(2*eps-X0)/Xh/C
	return abs(R)*abs(R)


# начинается расчет
px=[]
py=[]
py_hwidth = []



shag_itta = math.radians(float(8)/3600) # колличество точек по Длинне волны #-*-на входе-*-
itta_1 = 0.996 # предел интегрирования от
itta_2 = 1.01# предел интегрирования до


shag_teta = math.radians(float(2)/3600) # колличество точек по тета #-*-на входе-*-
teta_1 = (S2-S1)/(2*L12)
teta_2 = (S2+S1)/(2*L12)


dTeta_shag = math.radians(float(1)/3600) #-*-на входе-*-
dTeta_1 = math.radians(float(-10)/3600) #-*-на входе-*-
dTeta_2 = math.radians(float(10)/3600) #-*-на входе-*-

# нормировка
A = integrate.quad(apparatnaya,-teta_2,teta_2)[0]
B = integrate.quad(g_lambd,itta_1,itta_2)[0]


dTeta = dTeta_1


# давайте посчитаем отдельно аппаратную функцию, чтобы каждый раз ее не пересчитывать в интеграле
teta = -teta_2
j=0 # по тета
f_teta = []
while teta <= teta_2:
	f_teta.append(apparatnaya(teta))
	teta = teta + shag_teta
	j=j+1	
#-------------------время расчета именьшилось в два раза------------------------------------

# давайте просчитаем спектральную а в интеграле будемм ее только вызывать
itta =  itta_1 
P_Rez = 0
i=0 
f_lambda = []
while itta <= itta_2:
	f_lambda.append(g_lambd(itta))
	itta = itta + shag_itta
	i=i+1	
#-------------------вресмя уменьшилось на 10 процентов
_startTime = time.time()# начальная точка для отсчета времени


ind_itta1 = 0
ind_itta2 = i-1
ind_teta1 = 0
ind_teta2 = j-1
while dTeta <= dTeta_2:
	# i - itta , 
	# j - teta
	I1 = 1/4*(f_teta[0]*f_lambda[0]*sample_curve(dTeta,-teta_2,itta_1)*monohromator_curve(-teta_2,itta_1)+
		f_teta[0]*f_lambda[ind_itta2]*sample_curve(dTeta,-teta_2,itta_2)*monohromator_curve(-teta_2,itta_2)+
		f_teta[ind_teta2]*f_lambda[0]*sample_curve(dTeta,teta_2,itta_1)*monohromator_curve(teta_2,itta_1)+
		f_teta[ind_teta2]*f_lambda[ind_itta2]*sample_curve(dTeta,teta_2,itta_2)*monohromator_curve(teta_2,itta_2))

	itta =  itta_1 
	I2=0
	for i in range(1,ind_itta2-1):
		itta = itta + shag_itta
		P1 = f_teta[ind_teta2]*f_lambda[i]*sample_curve(dTeta,teta_2,itta)*monohromator_curve(teta_2,itta)
		P2 = f_teta[0]*f_lambda[i]*sample_curve(dTeta,-teta_2,itta)*monohromator_curve(-teta_2,itta)
		I2 = I2 + P1 + P2
	
	I2 = I2/2


	teta =  -teta_2 
	I3=0
	for j in range(1, ind_teta2-1):
		teta = teta + shag_teta
		P1 = f_teta[j]*f_lambda[0]*sample_curve(dTeta,teta,itta_1)*monohromator_curve(teta,itta_1)
		P2 = f_teta[j]*f_lambda[ind_itta2]*sample_curve(dTeta,teta,itta_2)*monohromator_curve(teta,itta_2)
		I3 = I3 + P1 + P2
	
	I3 = I3/2


	itta =  itta_1
	I4 = 0 
	for i in range(1, ind_itta2-1):
		itta = itta + shag_itta
		teta =  -teta_2
		for j in range(1, ind_teta2-1):
			teta = teta + shag_teta
			P = f_teta[j]*f_lambda[i]*sample_curve(dTeta,teta,itta)*monohromator_curve(teta,itta)
			I4= I4 + P

	Rez = I1+I2+I3+I4


	px.append(math.degrees(dTeta)*3600) 
	py.append(math.log10(Rez*shag_itta*shag_teta/A/B))
	py_hwidth.append((Rez*shag_itta*shag_teta/A/B))
	dTeta = dTeta + dTeta_shag
#1------------полуширина-------------------------------------------------------------------------------------------------------
def max_in_list(lst):
		assert lst
		m = lst[0]
		for i in lst:
			if i > m:
				m = i
		return m

def min_in_list(lst):
	assert lst
	m = lst[0]
	for i in lst:
		if i < m:
			m = i
	return m

def null(lst):
	assert lst

	m = lst[0]
	for i in lst:
		if i > m:
			m = i
	for i in range(len(lst)):
		val = lst[i]
		if val == m:
			break

	return i

def valueOnHalf(lst):
	assert lst
	m = lst[0]
	for i in lst:
		if i > m:
			m = i
	m = m/2
	z=0
	x1 = 0
	x2 = 1
	for i in range(len(lst)):
		val = lst[i]
		if val > m and x1 == 0:
			x1 = i
			x2 = 0
		if x2 == 0 and val < m:
			x2 = i
	return [x1, x2]
#1-------------------------------------------------------------------------------------------------------------------

#вывести время расчета 

total_sec = abs(float(_startTime - time.time()))
total_minutes = 0
total_hours = 0

if total_sec > 60:
	total_minutes = int(total_sec/60)
	total_sec = total_sec - total_minutes*60

if total_minutes>60:
	total_hours = int(total_minutes/60)
	total_minutes = total_minutes - total_hours*60

half_max = px[valueOnHalf(py_hwidth)[1]]-px[valueOnHalf(py_hwidth)[0]]

