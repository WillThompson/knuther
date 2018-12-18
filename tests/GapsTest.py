from tests.StatTest import *

class GapsTest(StatTest):

	def __init__(self,data,number):
		self.number = number
		StatTest.__init__(self,data)
		self.setValues2()
		self.testName = "Gaps Test for \'" + str(number) + "\'"

	def setValues(self):
		self.values = ['Gaps not set yet.']

	def setValues2(self):
		self.values = ['Gaps of size ' + str(n) for n in range(0,len(self.counts))]

	def setCounts(self):

		r = self.DataSet.getRange()
		r = r[1] - r[0] + 1
		counts = [0]*(2*r + 1)

		# While not at the end of the sequence, create the pairs and classify them
		notAtEnd = True
		j = 0

		# Find first index of number
		while next(self.DataSet.data) != self.number:
			j += 1
		i = j
		# Go over the dataset to get all the indices of the number
		while(notAtEnd):
			try:
				while next(self.DataSet.data) != self.number:
					j += 1
				counts[min(j - i,2*r)] += 1
				i = j

			except StopIteration:
				notAtEnd = False
		self.counts = counts
		self.DataSet.resetIterator()


	def setExpected(self):

		r = self.DataSet.getRange()
		r = r[1] - r[0] + 1
		p = 1.0/r
		c = len(self.counts)
		expected = [p*((1 - p)**k) for k in range(0,c)]
		expected[c-1] = (1 - p)**(c-1)
		n = sum(self.counts)
		self.expected = [n*x for x in expected]
