from tests.StatTest import *

class FrequencyTest(StatTest):

	def __init__(self,data):
		StatTest.__init__(self,data)
		self.testName = "Frequency Test"

	def setValues(self):
		self.values = list(range(self.DataSet.getRange()[1]+1))

	def setCounts(self):
		self.counts = [0 for v in self.values]
		for j in self.DataSet.data:
			self.counts[j] += 1
		# Reset the iterator.
		self.DataSet.resetIterator()

	def setExpected(self):
		r = self.DataSet.getRange()
		r = r[1] - r[0] + 1
		self.expected = [float(self.DataSet.getSize())/r for j in range(0,r)]