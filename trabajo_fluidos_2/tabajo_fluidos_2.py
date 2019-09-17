import os
import scipy as sp
from scipy.interpolate import interp1d
import matplotlib.pyplot as plt
print 'Imported scipy as sp\n'

# ask for values
k = float(raw_input('\nK de grupo: '))

# placeholder for data
line_L = ''
line_A = ''
line_A_a = ''
line_Msub =	''
line_Msup =	''
line_Psub = ''
line_Psup = ''

print '\nPlaceholder ready'
print 'Starting...\n'

################### Calculo datos ###################

for x in sp.arange(0.0,2.2,0.2):
	a_ = 20.0 - (20.0 * x) + (10.0 * x **2.0)
	a_crit = a_ / 10
	
	print 'Building data: %f/2.0' % x

	Msub = 0.0
	Psub = 0.0
	Msup = 0.0
	Psup = 0.0

	# calculo mach y presiones
	for m in sp.arange(0.00001, 7.00001, 0.00001):

		rel_area = (1.0/m) * ( ( 1.0 + ( (1.0/2.0) * (k-1.0) * m**2.0 ) ) / ( (1.0/2.0) * (k+1.0) ) )**( (k+1.0) / ( 2.0 * (k-1.0) ) )
		if (abs( rel_area - a_ / 10.0) < 0.00005) and m < 1.0:

			p = 100.0 * ( 1.0 + ( (k-1.0) / 2.0 ) * m**2.0 ) ** ( (-k) / (k-1.0) )

			Msub = m
			Psub = p
			

		if (abs( rel_area - a_ / 10.0) < 0.00005) and m > 1.0:

			p = 100.0 * ( 1.0 + ( (k-1.0) / 2.0 ) * m**2.0 ) ** ( (-k) / (k-1.0) )

			Msup = m
			Psup = p

	# salida de datos
	line_L   = line_L   + ',%f' % x
	line_A   = line_A   + ',%f' % a_
	line_A_a = line_A_a + ',%f' % a_crit
	line_Msub =	line_Msub + ',%f' % Msub
	line_Psub = line_Psub + ',%f' % Psub
	line_Msup =	line_Msup + ',%f' % Msup
	line_Psup = line_Psup + ',%f' % Psup

################### datos a file ###################

# Datos
x = line_L[1:]
Psub = line_Psub[1:]
Psup = line_Psup[1:]
A = line_A[1:]

line_L = 'L' + line_L + '\n'
line_A = 'A' + line_A + '\n'
line_A_a = 'A/A*' + line_A_a + '\n'
line_Msub = 'M(sub)' + line_Msub + '\n'
line_Msup = 'M(sup)' + line_Msup + '\n'
line_Psub = 'P(sup)' + line_Psub + '\n'
line_Psup = 'P(sup)' + line_Psup + '\n'

# find current file path
path = os.path.dirname(os.path.realpath(__file__))

# create files to store generated data
calculos = open ('%s/calculos.csv' % path, 'wb+')

# guardar data en el csv
data = [line_L, line_A, line_A_a, line_Msub, line_Msup, line_Psub, line_Psup]
calculos.writelines(data)
calculos.close()

# datos para grafica
x = x.split(',')
Psub = Psub.split(',')
Psup = Psup.split(',')
A = A.split(',')

################### Calculo flujo masico ###################

x = [float(i) for i in x]
Psub = [float(i) for i in Psub]
Psup = [float(i) for i in Psup]
A = [float(i) for i in A]


# se asume T y P ambientes (datos suministrados por el profesor Manuel)
Po = 100.0
To = 300.0

# listas de datos
P = Psub[:6]
A_ = A[:6]
Masico = []
gasto_masico = []
masico_max = 0

# interpolacion de tabla
P_Po = [1, 0.98, 0.95, 0.9, 0.8, 0.7, 0.6, 0.5283]
fuc  = [0.0, 0.1978, 0.3076, 0.4226, 0.5607, 0.6303, 0.6769, 0.6847]
f = interp1d(P_Po, fuc)


# calculo gasto masico
for i in Psub[:6]:
	if i/100.0 <= 0.5283:
		gasto_masico.append(0.6847)
	else:
		gasto_masico.append(float(f(i/100.0)))

# calculo flujo masico
val = 0
for i in gasto_masico:
	M = (i * A[val] * Po *1000.0) / (10000.0 * (287 * To)**0.5 )
	Masico.append(M)
	if M > masico_max:
		masico_max = M
	val += 1

# convertir a string
gasto_masico = ','.join(str(i) for i in gasto_masico)
Masico = ','.join(str(i) for i in Masico)
masico_max = str(masico_max)

gasto_masico = 'Gasto Masico,' + gasto_masico + '\n'
Masico = 'Masico,' + Masico + '\n'
masico_max = 'Masico max,%s' % masico_max

# salida al file
calculos = open ('%s/calculos.csv' % path, 'ab+')
data = [gasto_masico, Masico, masico_max]
calculos.writelines(data)
calculos.close()

################### plot ###################

plt.plot(x, Psub[:6] + Psup[6:], color='green')
plt.plot(x, Psup[:6] + Psub[6:], color='blue')
plt.title('Grafico de Presiones')
plt.xlabel('Longitud')
plt.ylabel('Presion')
plt.legend(loc='best')
plt.autoscale(tight=True)
plt.grid()
plt.show()




