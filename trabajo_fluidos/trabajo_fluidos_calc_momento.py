import os
import math
import csv
import matplotlib.pyplot as plt

# ask for values
radio = float(raw_input('Radio de la tuberia: '))
peso = float(raw_input('Peso del bloque: '))
z0 = float(raw_input('Brazo del centro a la bisagra: '))
gamma = float(raw_input('Gamma: '))
brazo_peso = 1.0

# find current file path
path = os.path.dirname(os.path.realpath(__file__))

#create files to store generated data
variables = open ('%s/files/variables.tsv' % path, 'wb')
momento = open('%s/files/momento.txt' % path, 'wb')
momento_csv = open('%s/files/momento.csv' % path, 'wb')

variables.write('Radio:\t%f' % radio)
variables.write('\nPeso:\t%f' % peso)
variables.write('\nz0:\t%f' % z0)
variables.write('\nGamma:\t%f' % gamma)
variables.close()

#function for calculations
def calc_momento():

	ang = math.radians(tita)

	altura = radio - radio * math.cos(ang)

	distancia_brazo = z0 + radio - (altura/3)

	Fr = gamma * (altura/2) * (radio * radio * (ang - (math.sin(2 * ang)) /2 ))

	Mom_ = (Fr * distancia_brazo) - (peso * brazo_peso)

	return Mom_

# make calculations and store them in files
for tita in xrange(181):
	Momento = calc_momento()
	momento.write('Tita: %d Momento: %f\n' % (tita, Momento))
	momento_csv.write('%d,%f\n' % (tita, Momento))

# close files
momento.close()
momento_csv.close()

# initializes data matrix
data = [[],[]]

# function for extracting data from file
def get_data(filename):
	with open (filename, 'r') as csvfile:
		csvfilereader = csv.reader(csvfile)
		for row in csvfilereader:
			data[0].append(float(row[0]))
			data[1].append(float(row[1]))

# extract the data and fills the matrix
get_data('%s/files/momento.csv' % path)

# creates a simple graph 
plt.plot(data[0], data[1], color='green')
plt.title('Grafico de momento')
plt.xlabel('Tita')
plt.ylabel('Momento')
plt.autoscale(tight=True)
plt.grid()
plt.show()