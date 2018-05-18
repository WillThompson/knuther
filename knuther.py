from scipy.stats import chisquare
from scipy.special import comb
import itertools
import math

## -- HELPERS (MAIN IS BELOW) -- ##

class Dataset:

	@staticmethod
	def fileIterator(filename):
		f = open(filename,'r')
		for line in f:
			yield(int(line))

	def __init__(self,filename):

		self.filename = filename
		self.resetIterator()
		self.info = dict()
		self.computeGlobals()
		self.resetIterator()


	def __str__(self):
		return("statTest.Dataset object\nRange:\t{0} - {1}\nSize:\t{2}".format(self.info['min'],self.info['max'],self.info['size']))

	def getData(self):
		return self.data

	def getRange(self):
		return([self.info['min'],self.info['max']])

	def getSize(self):
		return(self.info['size'])

	def getFilename(self):
		return(self.filename)

	def resetIterator(self):
		self.data = self.fileIterator(self.filename)

	def computeGlobals(self):
		vector = [x for x in self.data]
		self.info['max'] = max(vector)
		self.info['min'] = min(vector)
		self.info['size'] = len(vector)



def getGroupsOfSize(n,dataset,shift=0):
	groups = [dataset.getData()[shift:][k:k+n] for k in range(0,dataset.getSize()) if k % n == 0]
	if(len(groups[-1]) < n):
		groups = groups[:-1]
	return(groups)

class StatTest:

	def __init__(self, data):
		self.DataSet = data
		self.setValues()
		self.setCounts()
		self.setExpected()
		self.computeP()
		self.testName = "Test name not specified."

	def computeP(self):
		self.testStatistic, self.pvalue = chisquare(self.counts,self.expected)

	def __str__(self):
		template = "{0}\tp-value: {1:.6f}"
		return(template.format(self.testName,self.pvalue))


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

class PermutationTest(StatTest):

	def __init__(self,data,permSize=3):
		self.permutationSize = permSize
		StatTest.__init__(self,data)
		self.testName = "Permutation Test"

	def setValues(self):
		self.values = list(["Order " + str(k) for k in range(1,math.factorial(self.permutationSize)+1)] + ["None"])

	def setCounts(self):
		self.counts = [0]*len(self.values)

		# While not at the end of the sequence, create the pairs and classify them
		notAtEnd = True
		while(notAtEnd):
			try:
				triplet = [next(self.DataSet.data) for i in range(0,self.permutationSize)]
				self.counts[self.classifyPermutation(triplet)] += 1
			except StopIteration:
				notAtEnd = False
		self.DataSet.resetIterator()

	def classifyPermutation(self,data):
		if len(set(data)) == self.permutationSize:
			f = 0
			r = self.permutationSize
			while(r > 1):
				data = data[0:r]
				s = data.index(max(data)) + 1
				f = r*f + s - 1
				data[r-1],data[s-1] = data[s-1],data[r-1]
				r = r - 1
			return(f)
		return(math.factorial(self.permutationSize))

	def setExpected(self):
		m = self.DataSet.getRange()
		m = m[1] - m[0] + 1
		t = self.permutationSize
		
		p = 1 - math.factorial(m)/(math.factorial(m - t)*(m**t))
		expected = [(1 - p)/math.factorial(t)]*(math.factorial(t)+1)
		expected[-1] = p
		total = sum(self.counts)
		self.expected = [total*e for e in expected]

class PokerTest(StatTest):

	def __init__(self,data,handSize=5):
		self.handSize = handSize
		StatTest.__init__(self,data)
		self.testName = "Poker Test"

	def setValues(self):
		self.values = list([str(k) + " unique numbers" for k in range(1,self.handSize+1)])

	def setCounts(self):
		self.counts = [0]*len(self.values)

		# While not at the end of the sequence, create the pairs and classify them
		notAtEnd = True
		while(notAtEnd):
			try:
				hand = [next(self.DataSet.data) for i in range(0,self.handSize)]
				self.counts[len(set(hand))] += 1
			except StopIteration:
				notAtEnd = False
		self.DataSet.resetIterator()

	def setExpected(self):
		d = self.DataSet.getRange()
		d = d[1] - d[0] + 1
		r = self.handSize
		
		p[k] = [math.factorial(d)/((d**k)*math.factorial(d - r))*sterling2(k,r) for k in range(1,self.handSize+1)]



class RunsTest(StatTest):


	def runUpCheck(n0,n1):
		return(n1 > n0)

	def runDownCheck(n0,n1):
		return(n1 < n0)

	def __init__(self,data,runsUp):
		StatTest.__init__(self,data)
		self.runsUp = runsUp
		if self.runsUp:
			self.testName = "Runs Up Test"
		else:
			self.testName = "Runs Down Test"

	def setValues(self):
		self.values = [ "Runs of length " + str(k) for k in range(self.DataSet.getRange()[1]+1)]

	def setCounts(self):
		d = self.DataSet.getRange()
		d = d[1] - d[0] + 1
		self.counts = [0]*d

		# While not at the end of the sequence, check to see if the next number in the sequence is
		notAtEnd = True
		counter = 0;
		prev = next(self.DataSet.data)
		while(notAtEnd):
			try:
				num = next(self.DataSet.data)
				if (num > prev):
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

		self.expected = [comb(d,r)/(d**r) - comb(d,r+1)/(d**(r+1)) for r in range(1,d+1)]
		n = sum(self.counts)
		self.expected = [n*x for x in self.expected]


# Add Gaps Test

## -- MAIN -- ##

import sys
def main(argv):
	# Load the data
	filename = argv[1]
	data = Dataset(filename)
	print(data)

	# Create and perform all the stat tests
	tests = []
	tests.append(FrequencyTest(data))
	tests.append(SerialTest(data,False))
	tests.append(SerialTest(data,True))
	tests.append(PermutationTest(data))
	tests.append(RunsTest(data,True))

	for tst in tests:
		print(tst)

if __name__ == '__main__':
	main(sys.argv)