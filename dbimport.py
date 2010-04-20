#for data
from google.appengine.ext import db
import csv,sys

class SurveyResponse(db.Model):
  survey_id = db.IntegerProperty()
  choice_id = db.IntegerProperty()
  question_name = db.StringProperty()
  order = db.IntegerProperty()
  preceptor_id = db.IntegerProperty()
  preceptor_name = db.StringProperty()
  site_name = db.StringProperty()

def ascii(unicode_csv_data):
    for line in unicode_csv_data:
        yield line.decode('ascii', 'ignore') 

def load_data():
  reader = csv.reader(ascii(open( 'export.csv', 'rb')))
  headerrow = reader.next()

  for row in reader:
    if len(filter(lambda c: len(c) == 0, row)) == 0:
      surveyResponse = SurveyResponse(
        survey_id = int(row[0]),
        choice_id = int(row[1]),
        question_name = row[2],
        order = int(row[3]),
        preceptor_id = int(row[4]),
        preceptor_name = row[5],
        site_name = row[6],
      )
      db.put(surveyResponse)
