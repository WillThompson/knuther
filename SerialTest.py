from FrequencyTest import *
import itertools

class SerialTest(FrequencyTest):

	def __init__(self,data,offset):
		self.offset = offset
		FrequencyTest.__init__(self,data)
		self.testName = "Serial Test Offset" if offset else "Serial Test"

	def setValues(self):
		v = list(range(self.DataSet.getRange()[1]+1))
		self.values = [list(x) for x in list(itertools.product(v,v))]

	def setCounts(self):
		if self.offset:
			# Iterate the dataset by one before doing the counts
			next(self.DataSet.data)

		self.counts = [0]*len(self.values)

		# While not at the end of the sequence, create the pairs and classify them
		notAtEnd = True
		while(notAtEnd):
			try:
				pair = [next(self.DataSet.data),next(self.DataSet.data)]
				self.counts[self.values.index(pair)] += 1
			except StopIteration:
				notAtEnd = False

		self.DataSet.resetIterator()


	def setExpected(self):
		r = self.DataSet.getRange()
		r = r[1] - r[0] + 1
		r = r*r
		self.expected = [float(sum(self.counts))/r for j in range(0,r)]
