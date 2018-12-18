from scipy.stats import chisquare

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