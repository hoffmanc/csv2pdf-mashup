import csv
import sys
from pygooglechart import GroupedVerticalBarChart

#headerrow = reader.next()
#survey_id, choice_id, question_name, order, preceptor_id, site_name

#chart = GroupedVerticalBarChart(settings.width, settings.height,
#    y_range=(

def getaverageforfield(data, key, value):
    k = None
    for r in sorted(data, key=lambda rows: rows[key]):
        if k != r[key]:
            if k != None: yield (k, s/c)
            k = r[key]
            s = 0
            c = 0
        s += float(r[value])
        c += float(1)

if __name__ == "__main__":
    reader = csv.reader(open( sys.argv[1], 'rb' ))

    print "averages by question"
    for key, avg in getaverageforfield(reader, key=2, value=1):
        print "%s: %f" % (key, avg)

    reader = csv.reader(open( sys.argv[1], 'rb' ))
    print "averages by preceptor and question"
    #for key, avg in getaverageforfield(reader, key=tuple([5,2j), value=1):
        #    print "%s: %f" % (key, avg)

    a = [1,2,3,4]
    print a[2]
    print a[tuple([2,3])]
