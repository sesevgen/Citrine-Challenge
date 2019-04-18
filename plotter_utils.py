import argparse
import os.path
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def parse_input_plotter():
	"""
	Parses inputs to the plotter function, performing some common sense asserts and returns the output file to read from and the dimensions to plot.
	"""

	parser = argparse.ArgumentParser(description='This script plots generated vectors using a subset of their dimensions, in 1D, 2D or 3D as a way to quickly check point spread. Many localized clusters indicates poor sampling, whereas well distibuted points indicates good sampling.')
	parser.add_argument('output_file',help='Name of the file containing generated vectors.')
	parser.add_argument('dimensions',help='Dimensions to plot. Should have 1, 2 or 3 integers.',nargs='+')
	
	args = parser.parse_args()
	output_file = args.output_file
	try:
		dimensions = [int(dim) for dim in args.dimensions]
	except TypeError:
		print('Please provide integers for dimensions')

	assert ((len(dimensions) <= 3) and (len(dimensions) >= 0)), "Please provide 1, 2 or 3 integers for dimension"
	assert os.path.isfile(output_file), "File not found."

	print('Plotting vectors from '+output_file+' in the following dimension(s):',dimensions)	

	return output_file, dimensions


def load_array(output_file,dimensions):
	"""
	Returns a numpy array with the desired dimensions, read from provided file.
	"""
	fullarray = np.loadtxt(output_file)
	array = np.zeros((fullarray.shape[0],len(dimensions)))
	for i, dim in enumerate(dimensions):
		array[:,i] = fullarray[:,dim]

	return array

def plot_1d(array,dimensions):
	"""
	Plots a single dimensional array
	"""
	plt.figure()
	plt.plot(array)
	plt.xlabel('Points')
	plt.ylabel(str(dimensions[0])+'th Dimension')
	plt.show()

def plot_2d(array,dimensions):
	"""
	Plots a two dimensional array
	"""
	plt.figure()
	plt.scatter(array[:,0],array[:,1])
	plt.xlabel(str(dimensions[0])+'th Dimension')
	plt.ylabel(str(dimensions[1])+'th Dimension')
	plt.show()

def plot_3d(array,dimensions):
	"""
	Plots a three dimensional array
	"""
	plt.figure()
	ax = plt.axes(projection='3d')
	ax.scatter3D(array[:,0],array[:,1],array[:,2])
	ax.set_xlabel(str(dimensions[0])+'th Dimension')
	ax.set_ylabel(str(dimensions[1])+'th Dimension')
	ax.set_zlabel(str(dimensions[2])+'th Dimension')
	plt.show()
