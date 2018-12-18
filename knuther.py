from scipy.stats import chisquare
from scipy.special import comb
import itertools
import math

import Dataset
import tests.FrequencyTest
import tests.SerialTest
import tests.PermutationTest
import tests.PokerTest
import tests.RunsTest
import tests.GapsTest

## -- MAIN -- ##

import sys
def main(argv):
	# Load the data
	filename = argv[1]
	data = Dataset.Dataset(filename)
	print(data)

	# Create the statTest objects and put them in a list
	test_list = []
	test_list.append(tests.FrequencyTest.FrequencyTest(data))
	test_list.append(tests.SerialTest.SerialTest(data,False))
	test_list.append(tests.SerialTest.SerialTest(data,True))
	test_list.append(tests.PokerTest.PokerTest(data))
	test_list.append(tests.PermutationTest.PermutationTest(data))
	test_list.append(tests.RunsTest.RunsTest(data,True))
	test_list.append(tests.RunsTest.RunsTest(data,False))
	for k in range(data.getRange()[0],data.getRange()[1]+1):
		test_list.append(tests.GapsTest.GapsTest(data,k))

	for tst in test_list:
		print(tst)

if __name__ == '__main__':
	main(sys.argv)