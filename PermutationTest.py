from StatTest import *
import math

class PermutationTest(StatTest):

	def __init__(self, data, permSize=3):
		self.permutationSize = permSize
		StatTest.__init__(self, data)
		self.testName = "Permutation Test"

	def setValues(self):
		self.values = list(["Order " + str(k) for k in range(1, math.factorial(self.permutationSize) + 1)] + ["None"])

	def setCounts(self):
		self.counts = [0] * len(self.values)

		# While not at the end of the sequence, create the pairs and classify them
		notAtEnd = True
		while (notAtEnd):
			try:
				triplet = [next(self.DataSet.data) for i in range(0, self.permutationSize)]
				self.counts[self.classifyPermutation(triplet)] += 1
			except StopIteration:
				notAtEnd = False
		self.DataSet.resetIterator()

	def classifyPermutation(self, data):
		if len(set(data)) == self.permutationSize:
			f = 0
			r = self.permutationSize
			while (r > 1):
				data = data[0:r]
				s = data.index(max(data)) + 1
				f = r * f + s - 1
				data[r - 1], data[s - 1] = data[s - 1], data[r - 1]
				r = r - 1
			return (f)
		return (math.factorial(self.permutationSize))

	def setExpected(self):
		m = self.DataSet.getRange()
		m = m[1] - m[0] + 1
		t = self.permutationSize

		p = 1 - math.factorial(m) / (math.factorial(m - t) * (m ** t))
		expected = [(1 - p) / math.factorial(t)] * (math.factorial(t) + 1)
		expected[-1] = p
		total = sum(self.counts)
		self.expected = [total * e for e in expected]
