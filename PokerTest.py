from StatTest import *
import math

def sterling2(n,k):
	if k == n:
		return(1)
	elif k == 0 or n == 0:
		return(0)
	elif k == n-1:
		return(n*(n-1)/2)
	else:
		return k*sterling2(n-1,k) + sterling2(n-1,k-1)



class PokerTest(StatTest):

	def __init__(self, data, handSize=5):
		self.handSize = handSize
		StatTest.__init__(self, data)
		self.testName = "Poker Test"

	def setValues(self):
		self.values = list([str(k) + " unique numbers" for k in range(1, self.handSize + 1)])

	def setCounts(self):
		self.counts = [0] * len(self.values)

		# While not at the end of the sequence, create the pairs and classify them
		notAtEnd = True
		while (notAtEnd):
			try:
				hand = [next(self.DataSet.data) for i in range(0, self.handSize)]
				self.counts[len(set(hand))-1] += 1
			except StopIteration:
				notAtEnd = False
		self.DataSet.resetIterator()

	def setExpected(self):
		d = self.DataSet.getRange()
		d = d[1] - d[0] + 1
		k = self.handSize
		p = [math.factorial(d) / ((d ** k) * math.factorial(d - rr)) * sterling2(k, rr) for rr in range(1, self.handSize + 1)]
		self.expected = [sum(self.counts)*pp for pp in p]
