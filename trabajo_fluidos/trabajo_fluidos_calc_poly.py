import os
import math
import scipy as sp
import scipy.optimize as optimize
import matplotlib.pyplot as plt

# importing data from csv file
path = os.path.dirname(os.path.realpath(__file__))
data = sp.genfromtxt('%s/files/momento.csv' % path, delimiter= ',')

# printing first 10 rows in data file
print 'First 10 rows in data file:\n', data[:10]
# print the shape of the matrix
print '\nShape of the matrix:', data.shape

# separating the data by columns
x = data[:,0]
y = data[:,1]

# checking for invalid numbers in data
invalid_num = sp.sum(sp.isnan(y))
print 'Invalid numbers in data: %i' % invalid_num

# negating invalid values from data
# use only when they represent less than 3% of data
if invalid_num > 1:
	x = x[~sp.isnan(y)]
	y = y[~sp.isnan(y)]

# function for recording error between poly and actual data
def error(f, x, y):
	return sp.sum((f(x) - y) **2)

# finds parameters for the function with polyfit
# then creates the function with poly1d
f1 = sp.poly1d(sp.polyfit(x, y, 1))
f2 = sp.poly1d(sp.polyfit(x, y, 2))
f3 = sp.poly1d(sp.polyfit(x, y, 3))
f4 = sp.poly1d(sp.polyfit(x, y, 4))

'''lets create a function of second order
only with 10 values around the inflection point'''
for row in xrange(182):
	row_ = row
	if abs(y[row]) == y[row]:
		break

if row_ == 182:
	print '\n\n###\nNo inflection point detected in data,\nplease check initial values\n###\n\n'
	quit()

x1 = x[(row_ - 10) : (row_ + 10)]
y1 = y[(row_ - 10) : (row_ + 10)]

# calculate poly and poly root
f_inflec = sp.poly1d(sp.polyfit(x1, y1, 3))
bisect = optimize.bisect(f_inflec, (row_ - 5), (row_ + 5))

# calculate hight 
variables = sp.genfromtxt('%s/files/variables.tsv' % path, delimiter= '\t')
radio = variables[0,1]
print radio
altura = radio - radio * math.cos(math.radians(bisect))

# write info to file
poly_file = open('%s/files/polynomial_equ.txt' % path, 'wb')
poly_file.write('Polynomial equation generated with 20 values around the inflection point:\n')
poly_file.write(str(f_inflec))
poly_file.write('\nError(f_inflec): %f (over the 20 values selected)' % error(f_inflec, x1, y1))
poly_file.write('\nBisection: %f' % bisect)
poly_file.write('\nAltura a la que abre: %f' % altura)
poly_file.close()

# prints the parameters for the function
print '\n-----------\nModel parameters(f1):\n %s \n' % f1
print '-----------\nModel parameters(f2):\n %s \n' % f2
print '-----------\nModel parameters(f3):\n %s \n' % f3
print '-----------\nModel parameters(f4):\n %s \n' % f4
print '-----------\nModel parameters(f_inflec):\n %s \n----' % f_inflec
print 'Biseccion: %f \n----' % bisect
print 'Altura a la que abre: %f \n-----------' % altura

# prints the error of the function
print 'Error(f1): %f' % error(f1, x, y)
print 'Error(f2): %f' % error(f2, x, y)
print 'Error(f3): %f' % error(f3, x, y)
print 'Error(f4): %f' % error(f4, x, y)
print 'Error(f_inflec): %f (over the 20 values selected)\n-----------\n-----------\n\n' % error(f_inflec, x1, y1)

# generate x-values for plotting
fx = sp.linspace(-5, 185, num= 95)
fx1 = sp.linspace(-5, 185, num= 190)

# creates plot
# labels and titles are in Spanish
plt.plot( x, y,label='Curva de momento',color='green',linewidth=5)
plt.plot( fx1, f_inflec(fx1),label='f_inflec',color='yellow',linewidth=2)
plt.plot( fx, f1(fx),label='Orden = %i' % f1.order,color='blue',linestyle='dashed',linewidth=1)
plt.plot( fx, f2(fx),label='Orden = %i' % f2.order,color='red',linestyle='dashed',linewidth=1)
plt.plot( fx, f3(fx),label='Orden = %i' % f3.order,color='purple',linestyle='dashed',linewidth=1)
plt.plot( fx, f4(fx),label='Orden = %i' % f4.order,color='orange',linestyle='dashed',linewidth=1)
plt.scatter(bisect, f_inflec(bisect),label='Biseccion',marker='o',linewidth=8)
plt.legend(loc='upper left')
plt.title('Grafico de momento')
plt.xlabel('Tita')
plt.ylabel('Momento')
plt.autoscale(tight=True)
plt.grid()
plt.show()