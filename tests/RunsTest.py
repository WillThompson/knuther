from tests.StatTest import *
from scipy.special import comb

def checkup(x, y):
	return x > y

def checkdown(x, y):
	return x < y


class RunsTest(StatTest):

	def __init__(self, data, runsUp):
		self.runsUp = runsUp
		self.check = checkup if runsUp else checkdown
		StatTest.__init__(self, data)
		self.testName = "Runs Up Test" if runsUp else "Runs Down Test"

	def setValues(self):
		self.values = ["Runs of length " + str(k) for k in range(self.DataSet.getRange()[1] + 1)]

	def setCounts(self):
		d = self.DataSet.getRange()
		d = d[1] - d[0] + 1
		self.counts = [0] * d

		# While not at the end of the sequence, check to see if the next number in the sequence is
		notAtEnd = True
		counter = 0;
		prev = next(self.DataSet.data)
		while (notAtEnd):
			try:
				num = next(self.DataSet.data)
				if (self.check(num, prev)):
					prev = num
					counter += 1
				else:
					self.counts[counter] += 1
					counter = 0;
					prev = next(self.DataSet.data)

			except StopIteration:
				notAtEnd = False

		# With run sizes counted, reset the iterator
		self.DataSet.resetIterator()

	def setExpected(self):
		d = self.DataSet.getRange()
		d = d[1] - d[0] + 1
		n = sum(self.counts)

		self.expected = [comb(d, r) / (d ** r) - comb(d, r + 1) / (d ** (r + 1)) for r in range(1, d + 1)]
		n = sum(self.counts)
		self.expected = [n * x for x in self.expected]