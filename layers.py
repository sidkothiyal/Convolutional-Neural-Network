import math
import random

#TODO bias and bias wt

def softmax(output_layer_vals):
	softmax_vals = []
	sum_of_vals = 0
	max_val = 0
	for output_layer_val in output_layer_vals:
		if max_val < output_layer_val:
			max_val = output_layer_val

	for i, output_layer_val in enumerate(output_layer_vals):
		sum_of_vals += math.exp(output_layer_val - max_val)
	
	for i, output_layer_val in enumerate(output_layer_vals):
		softmax_vals.append(math.exp(output_layer_val - max_val)/sum_of_vals)

	return softmax_vals	

def derivative_softmax(x):
	return x * (1-x)

def leaky_relu(x):
	if x < 0:
		return 0.01 *x
	else:
		return x	

def derivative_leaky_relu(x):
	if x < 0:
		return 0.001
	else:
		return 1
			
def output_function(x):
	return 1/(1 + math.exp(-x))

def derivative_output_function(x):
	return math.exp(x)/((1-math.exp(x)) * (1-math.exp(x)))	

def output_summation(layer, i):
	sum = 0
	for neuron in layer.neurons:
		#print neuron
		sum += neuron.get_summation(i)
	return sum


class HiddenLayer:
	bias = 1
	neurons = []
	prevLayer = None
	nextLayer = None
	inputSummation = []

	def __init__(self, hidden_layer_size):
		self.size = hidden_layer_size

	def calc_neuron_vals(self):
		self.inputSummation = []
		for i, neuron in enumerate(self.neurons):
			self.inputSummation.append(output_summation(self.prevLayer, i) + self.bias)
			neuron.value = output_function(self.inputSummation[-1])
			#print "val ", neuron.value

	def set_architecture(self, prevLayer, nextLayer):
		self.prevLayer = prevLayer
		self.nextLayer = nextLayer
		bias = 0.5
		for i in xrange(self.size):
			self.neurons.append(Neuron())
			for j, neuron in enumerate(self.prevLayer.neurons):
				neuron.outgoing_weights.append(random.uniform(0, 1))

	def change_weights(self, rate):
		for i, neuron in enumerate(self.neurons):
			neuron.error = derivative_output_function(self.inputSummation[i])
			sumNextErrors = 0
			for j, nextNeuron in enumerate(self.nextLayer.neurons):
				sumNextErrors += neuron.outgoing_weights[i] * nextNeuron.error
			neuron.error *= sumNextErrors
			for j, prevNeuron in enumerate(self.prevLayer.neurons):
				weightDiff = rate * neuron.error * prevNeuron.value
				prevNeuron.outgoing_weights[i] += weightDiff	

class InputLayer:
	neurons = []
	nextLayer = None
	def __init__(self, size):
		self.size = size

	def set_architecture(self, nextLayer):
		for i in xrange(self.size):
			self.neurons.append(Neuron())
		self.nextLayer = nextLayer	

	def put_values(self, feature_vector):
		for i, feature in enumerate(feature_vector):
			self.neurons[i].value = feature


class OutputLayer:
	bias = 1
	neurons = []
	prevLayer = None
	inputSummation = []

	def __init__(self, output_size):
		self.size = output_size

	def calc_neuron_vals(self):
		self.inputSummation = []
		for i, neuron in enumerate(self.neurons):
			#print output_summation(self.prevLayer, i)
			self.inputSummation.append(output_summation(self.prevLayer, i) + self.bias)
		neuron_vals = softmax(self.inputSummation)
		for i, neuron in enumerate(self.neurons):
			neuron.value = neuron_vals[i]

	def set_architecture(self, hiddenLayer):
		self.prevLayer = hiddenLayer
		bias = 0.5
		for i in xrange(self.size):
			self.neurons.append(Neuron())
			for j, neuron in enumerate(self.prevLayer.neurons):
				neuron.outgoing_weights.append(random.uniform(0, 1))

	def put_values(self, expected_output):
		self.expected_output = expected_output

	def output_diff(self):
		diff = []
		for i in xrange(self.size):
			diff.append(self.expected_output[i] - self.neurons[i].value)
		return diff

	def get_output(self):
		max_val = 0
		max_pos = 0
		for i, neuron in enumerate(self.neurons):
			if max_val < neuron.value:
				max_val = neuron.value
				max_pos = i
		inps = ['frog', 'bird', 'airplane', 'dog', 'deer', 'truck', 'automobile', 'horse', 'cat', 'ship']
		return inps[max_pos]

	def change_weights(self, rate):
		diff = self.output_diff()
		#print "diff ", diff
		for i, neuron in enumerate(self.neurons):
			neuron.error = diff[i] * derivative_softmax(neuron.value)
			#print self.inputSummation[i]
			for j, prevNeuron in enumerate(self.prevLayer.neurons):
				weightDiff = rate * neuron.error * prevNeuron.value
				#print weightDiff
				prevNeuron.outgoing_weights[i] += weightDiff


class Neuron:
	value = 0
	outgoing_weights = []
	error = 0
	def __init__(self):
		pass

	def get_summation(self, i):
		return self.value * self.outgoing_weights[i]