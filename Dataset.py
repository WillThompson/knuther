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
