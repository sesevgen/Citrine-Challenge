import argparse
import os.path
import numpy as np

def parse_input_sampler():
	"""
	Parses inputs to the sampler function, performing some common sense asserts and returns the input file to read from, output file to write to, and the number of points to generate.
	"""

	parser = argparse.ArgumentParser(description='This script generates vectors in n-dimensional space within the unit hypercube subject to constraints provided as python expressions from an input file. Requires a seed point, ideally within the constraints.')


	parser.add_argument('input_file', help='Name of the input file containing dimensionality and constraints')
	parser.add_argument('output_file', help='Name of the output file to export generated points to')
	parser.add_argument('n_results', help='Number of points to generate', type=int)
	parser.add_argument('-f','--format', nargs='?', default = '%10.10f', help='Formatting of the output. Default = %%10.10f')
	parser.add_argument('-d','--decay', nargs='?', default = 0.99, type=float, 
		help='Decay of random walk step size per failure. Should be between 0 and 1. Higher values slow point generation but increase point spread and chance of ergodicity. Default = 0.99')
	parser.add_argument('-s','--steps',nargs='?', default = 20, type=int, 
		help='Number of random walk steps to attempt per point. Higher values speed up point generation but also cause points to be more clustered. Default = 20')
	parser.add_argument('-r','--reset',nargs='?', default = 'zero',
		help='Options: zero or decrement - Mode to reset random walk step length. \'zero\' resets random walk step length on a success. \'decrement\' decrements failure counter by 1. \'decrement\' is significantly faster, but also generates significantly more correlated samples. Default = \'zero\' ')
	parser.add_argument('-b','--benchmark',nargs='?', default=False,
		help='If enabled, keeps track of the sampling portion of runtime and reports it.')


	args = parser.parse_args()
	input_file = args.input_file
	assert os.path.isfile(input_file), "File not found."
	output_file = args.output_file
	n_results = args.n_results
	assert args.reset == 'zero' or args.reset == 'decrement' 
	optional_args={ 'format': args.format,
			'decay' : args.decay,
			'steps': args.steps,
			'reset': args.reset,
			'benchmark':args.benchmark}


	print(('Generating {} points, subject to constraints from '+input_file+', and writing the results to '+output_file+'.').format(n_results))

	return input_file, output_file, n_results, optional_args

def write_output(output_file,container,fmt='%10.10f'):
	try:
		np.savetxt(output_file,np.array(container),fmt=fmt)
	except ValueError:
		print('Error reading format. Defaulting to standard formatting of %10.10f')
		np.savetxt(output_file,np.array(container),fmt='%10.10f')

	print('Results comprised of {} vectors written to '.format(len(container))+output_file)

def run_check(container,constraints):
	"""
	Checks that all vectors in the container obey constraints and are within the unit hypercube. Returns a boolean and a list of failed points, if any.
	"""

	print('Running final check on generated vectors, ensuring all are within the unit hypercube and obey constraints.')
	
	passed = True

	failures = []
	for i, vector in enumerate(container):
		for coord in vector:
			if coord < 0.0 or coord > 1.0:
				failures.append(i)
				passed = False
		if not constraints.apply(vector):
			failures.append(i)
			passed = False

	if passed:
		print('Final check completed successfully. All points are within the unit hypercube and obey constraints.')
	
	else:
		print('Final check failed. Failure at entries: ',failures)

	return passed, failures		
