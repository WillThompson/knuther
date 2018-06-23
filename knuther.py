from scipy.stats import chisquare
from scipy.special import comb
import itertools
import math

from Dataset import *
from FrequencyTest import *
from SerialTest import *
from PermutationTest import *
from PokerTest import *
from RunsTest import *
from GapsTest import *

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
	tests.append(PokerTest(data))
	tests.append(PermutationTest(data))
	tests.append(RunsTest(data,True))
	tests.append(RunsTest(data,False))
	for k in range(data.getRange()[0],data.getRange()[1]+1):
		tests.append(GapsTest(data,k))

	for tst in tests:
		print(tst)

if __name__ == '__main__':
	main(sys.argv)