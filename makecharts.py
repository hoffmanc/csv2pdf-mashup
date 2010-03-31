import csv
import sys
from pygooglechart import GroupedVerticalBarChart

from itertools import izip
reader = csv.reader(open( sys.argv[1], 'r' ))
headerrow = reader.next()

print headerrow
print reader.next()
