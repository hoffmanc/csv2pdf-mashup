import csv
import sys
from pygooglechart import GroupedVerticalBarChart
from operator import itemgetter
from itertools import groupby

def average(data, key=itemgetter(0), value=itemgetter(1)):
    """Summarise the supplied data.

       Produce a summary of the data, grouped by the given key (default: the
       first item), and giving totals of the given value (default: the second
       item).

       The key and value arguments should be functions which, given a data
       record, return the relevant value.
    """
    for k, group in groupby(data, key):
        yield (k, sum(value(row) for row in group) / count(group)

if __name__ == "__main__":
    reader = csv.reader(open( sys.argv[1], 'rb' ))
  #headerrow = reader.next()
  #survey_id, choice_id, question_name, order, preceptor_id, site_name

  #chart = GroupedVerticalBarChart(settings.width, settings.height,
  #    y_range=(

    rows = []
    for r in reader:
        rows.append((r[2], float(r[1])))

    for question, avg in average(rows):
        print "%10s: %d" % (question, avg)

